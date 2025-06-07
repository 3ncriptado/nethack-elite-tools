import tkinter as tk
import customtkinter as ctk
import socket
import threading
import time
import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
import re
from urllib.parse import urlparse
matplotlib.use("TkAgg")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class NetworkToolsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NetHack Elite Tools")
        self.geometry("1200x700")

        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Crear sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#0a0a0a")
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="NetHack\nElite Tools", 
                                       font=ctk.CTkFont(size=24, weight="bold"), text_color="#00ff00")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        buttons = [
            ("Resolver IP", self.show_resolver),
            ("Port Check", self.show_port_check),
            ("Hosting Info", self.show_hosting),
            ("Port Ping", self.show_portping),
            ("FiveM Check", self.show_fivem_check)
        ]

        for i, (text, command) in enumerate(buttons, start=1):
            btn = ctk.CTkButton(self.sidebar_frame, text=text, command=command, 
                                fg_color="transparent", text_color="#00ff00", 
                                hover_color="#1a1a1a", anchor="w")
            btn.grid(row=i, column=0, padx=20, pady=10, sticky="ew")

        # Crear frame principal
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a1a")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=28, weight="bold"), text_color="#00ff00")
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="nw")

        # Inicializar componentes
        self.setup_resolver()
        self.setup_port_check()
        self.setup_hosting()
        self.setup_portping()
        self.setup_fivem_check()

        # Mostrar frame inicial
        self.show_resolver()

        # Variables para FiveM Check
        self.fivem_cfx_url = None
        self.fivem_port = None

    def show_frame(self, frame, title):
        self.hide_all_frames()
        frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.title_label.configure(text=title)

    def show_resolver(self):
        self.show_frame(self.resolver_frame, "Resolver IP")

    def show_port_check(self):
        self.show_frame(self.port_check_frame, "Port Check")

    def show_hosting(self):
        self.show_frame(self.hosting_frame, "Hosting Info")

    def show_portping(self):
        self.show_frame(self.portping_frame, "Port Ping")

    def show_fivem_check(self):
        self.show_frame(self.fivem_check_frame, "FiveM Check")

    def hide_all_frames(self):
        for frame in [self.resolver_frame, self.port_check_frame, self.hosting_frame, self.portping_frame, self.fivem_check_frame]:
            frame.grid_forget()

    def create_input_field(self, parent, placeholder):
        return ctk.CTkEntry(parent, placeholder_text=placeholder, fg_color="#0a0a0a", text_color="#00ff00", placeholder_text_color="#006400")

    def create_button(self, parent, text, command):
        return ctk.CTkButton(parent, text=text, command=command, fg_color="#006400", hover_color="#008000", text_color="white")

    def create_output_field(self, parent):
        output = ctk.CTkTextbox(parent, fg_color="#0a0a0a", text_color="#00ff00")
        output.grid(sticky="nsew", padx=20, pady=10)
        parent.grid_rowconfigure(parent.grid_size()[1]-1, weight=1)
        return output

    def setup_resolver(self):
        self.resolver_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.resolver_frame.grid_columnconfigure(0, weight=1)
        self.resolver_frame.grid_rowconfigure(2, weight=1)
        
        self.domain_entry = self.create_input_field(self.resolver_frame, "Enter domain")
        self.domain_entry.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        self.create_button(self.resolver_frame, "Resolve", self.resolve_domain).grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        self.resolver_result = self.create_output_field(self.resolver_frame)
        self.resolver_result.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

    def setup_port_check(self):
        self.port_check_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.port_check_frame.grid_columnconfigure(0, weight=1)
        self.port_check_frame.grid_rowconfigure(2, weight=1)
        
        self.port_check_host = self.create_input_field(self.port_check_frame, "Enter domain or IP")
        self.port_check_host.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        self.create_button(self.port_check_frame, "Check Ports", self.check_ports).grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        self.port_check_result = self.create_output_field(self.port_check_frame)
        self.port_check_result.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

    def setup_hosting(self):
        self.hosting_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.hosting_frame.grid_columnconfigure(0, weight=1)
        self.hosting_frame.grid_rowconfigure(2, weight=1)
        
        self.hosting_host = self.create_input_field(self.hosting_frame, "Enter domain or IP")
        self.hosting_host.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        self.create_button(self.hosting_frame, "Get Hosting Info", self.check_hosting).grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        self.hosting_result = self.create_output_field(self.hosting_frame)
        self.hosting_result.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

    def setup_portping(self):
        self.portping_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.portping_frame.grid_columnconfigure(0, weight=1)
        self.portping_frame.grid_rowconfigure(4, weight=1)
        
        self.portping_host = self.create_input_field(self.portping_frame, "Enter domain or IP")
        self.portping_host.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        self.portping_port = self.create_input_field(self.portping_frame, "Port")
        self.portping_port.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        self.portping_button = self.create_button(self.portping_frame, "Start Port Ping", self.toggle_portping)
        self.portping_button.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        
        self.portping_result = self.create_output_field(self.portping_frame)
        self.portping_result.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
        
        # Setup for graph
        self.fig, self.ax = plt.subplots(figsize=(5, 3), facecolor='#1a1a1a')
        self.ax.set_facecolor('#1a1a1a')
        self.ax.tick_params(axis='x', colors='#00ff00')
        self.ax.tick_params(axis='y', colors='#00ff00')
        self.ax.set_xlabel('Time', color='#00ff00')
        self.ax.set_ylabel('Response Time (ms)', color='#00ff00')
        self.ax.set_title('Port Ping Response Time', color='#00ff00')
        
        for spine in self.ax.spines.values():
            spine.set_edgecolor('#00ff00')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.portping_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=4, column=0, sticky="nsew", padx=20, pady=10)
        
        self.ping_times = []
        self.is_pinging = False

    def setup_fivem_check(self):
        self.fivem_check_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.fivem_check_frame.grid_columnconfigure(0, weight=1)
        self.fivem_check_frame.grid_rowconfigure(3, weight=1)
        
        self.fivem_url = self.create_input_field(self.fivem_check_frame, "Enter FiveM URL (cfx.re/join/XXXX)")
        self.fivem_url.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        self.create_button(self.fivem_check_frame, "Check FiveM Server", self.check_fivem).grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        self.fivem_result = self.create_output_field(self.fivem_check_frame)
        self.fivem_result.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

        self.fivem_portping_button = self.create_button(self.fivem_check_frame, "Port Ping CFX URL", self.redirect_to_portping)
        self.fivem_portping_button.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        self.fivem_portping_button.configure(state="disabled")

    def resolve_domain(self):
        domain = self.domain_entry.get()
        try:
            ip = socket.gethostbyname(domain)
            self.resolver_result.delete("0.0", "end")
            self.resolver_result.insert("0.0", f"IP: {ip}")
        except socket.gaierror:
            self.resolver_result.delete("0.0", "end")
            self.resolver_result.insert("0.0", "Failed to resolve domain")

    def check_ports(self):
        host = self.port_check_host.get()
        ports = [80, 443, 30120, 30121]
        self.port_check_result.delete("0.0", "end")
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                self.port_check_result.insert("end", f"Port {port}: Open\n")
            else:
                self.port_check_result.insert("end", f"Port {port}: Closed\n")
            sock.close()

    def check_hosting(self):
        host = self.hosting_host.get()
        try:
            response = requests.get(f"http://{host}", timeout=5)
            server = response.headers.get('Server', 'Unknown')
            self.hosting_result.delete("0.0", "end")
            self.hosting_result.insert("0.0", f"Server: {server}")
        except requests.RequestException:
            self.hosting_result.delete("0.0", "end")
            self.hosting_result.insert("0.0", "Failed to get hosting information")

    def toggle_portping(self):
        if self.is_pinging:
            self.is_pinging = False
            self.portping_button.configure(text="Start Port Ping")
        else:
            # Validate the port before starting the ping thread
            try:
                int(self.portping_port.get())
            except ValueError:
                self.portping_result.delete("0.0", "end")
                self.portping_result.insert(
                    "0.0", "Invalid port. Please enter a valid integer."
                )
                return

            self.is_pinging = True
            self.portping_button.configure(text="Stop Port Ping")
            self.ping_times = []
            threading.Thread(target=self.run_portping, daemon=True).start()

    def run_portping(self):
        host = self.portping_host.get()
        try:
            port = int(self.portping_port.get())
        except ValueError:
            # Invalid port provided
            self.portping_result.delete("0.0", "end")
            self.portping_result.insert(
                "0.0", "Invalid port. Please enter a valid integer."
            )
            self.is_pinging = False
            self.portping_button.configure(text="Start Port Ping")
            return
        self.portping_result.delete("0.0", "end")
        try:
            ip = socket.gethostbyname(host)
        except socket.gaierror:
            ip = "Unable to resolve IP"
        
        while self.is_pinging:
            start_time = time.time()
            try:
                with socket.create_connection((host, port), timeout=1) as sock:
                    end_time = time.time()
                    duration = (end_time - start_time) * 1000  # Convert to milliseconds
                    self.ping_times.append(duration)
                    self.portping_result.insert("end", f"Response from: {ip}/{host} to port {port} - Time: {duration:.2f}ms\n")
                    self.portping_result.see("end")
            except (socket.timeout, ConnectionRefusedError):
                self.ping_times.append(0)  # 0 ms indicates failure
                self.portping_result.insert("end", f"No response from: {ip}/{host} to port {port} - Timed out\n")
                self.portping_result.see("end")
            except Exception as e:
                self.ping_times.append(0)  # 0 ms indicates failure
                self.portping_result.insert("end", f"Error pinging {ip}/{host} on port {port}: {str(e)}\n")
                self.portping_result.see("end")
            
            self.update_graph()
            time.sleep(1)

    def update_graph(self):
        self.ax.clear()
        self.ax.plot(self.ping_times, color='#00ff00', linewidth=2)
        self.ax.set_facecolor('#1a1a1a')
        self.ax.tick_params(axis='x', colors='#00ff00')
        self.ax.tick_params(axis='y', colors='#00ff00')
        self.ax.set_xlabel('Time', color='#00ff00')
        self.ax.set_ylabel('Response Time (ms)', color='#00ff00')
        self.ax.set_title('Port Ping Response Time', color='#00ff00')
        for spine in self.ax.spines.values():
            spine.set_edgecolor('#00ff00')
        self.canvas.draw()

    def check_fivem(self):
        url = self.fivem_url.get().strip()
        
        # Add https:// if not present
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        # Ensure the URL starts with https://cfx.re/join/
        if not url.startswith("https://cfx.re/join/"):
            self.fivem_result.delete("0.0", "end")
            self.fivem_result.insert("0.0", "Invalid FiveM URL. It should be in the format 'cfx.re/join/XXXX'")
            return

        try:
            response = requests.get(url, allow_redirects=False)
            html_content = response.text
            headers = response.headers

            # Extract information from HTML
            title_match = re.search(r'<h1 title="([^"]+)"', html_content)
            players_match = re.search(r'<span class="players"><span class="material-icons">people_outline</span>\s*(\d+)</span>', html_content)

            # Extract information from headers
            server = headers.get('server', 'Unknown')
            join_token = headers.get('x-citizenfx-join-token', 'Unknown')
            cfx_url = headers.get('x-citizenfx-url', 'Unknown')

            # Store CFX URL for Port Ping
            self.fivem_cfx_url = cfx_url
            parsed_url = urlparse(cfx_url)
            self.fivem_port = parsed_url.port or 30120  # Default to 30120 if port is not specified

            # Prepare result
            result = f"Server Name: {title_match.group(1) if title_match else 'Unknown'}\n"
            result += f"Players: {players_match.group(1) if players_match else 'Unknown'}\n"
            result += f"Server: {server}\n"
            result += f"Join Token: {join_token}\n"
            result += f"CFX URL: {cfx_url}\n"

            self.fivem_result.delete("0.0", "end")
            self.fivem_result.insert("0.0", result)

            # Enable Port Ping button
            self.fivem_portping_button.configure(state="normal")
        except requests.RequestException as e:
            self.fivem_result.delete("0.0", "end")
            self.fivem_result.insert("0.0", f"Error checking FiveM server: {str(e)}")
            self.fivem_portping_button.configure(state="disabled")

    def redirect_to_portping(self):
        if self.fivem_cfx_url and self.fivem_port:
            parsed_url = urlparse(self.fivem_cfx_url)
            host = parsed_url.hostname
            
            self.show_portping()
            self.portping_host.delete(0, 'end')
            self.portping_host.insert(0, host)
            self.portping_port.delete(0, 'end')
            self.portping_port.insert(0, str(self.fivem_port))

if __name__ == "__main__":
    app = NetworkToolsApp()
    app.mainloop()