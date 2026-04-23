import click
import socket
import threading
from datetime import datetime
from opsforge.core.output import console

@click.command(name="honeypot")
@click.option("--ports", "-p", default="21,22,23,80,443,3306", help="Ports to listen on (comma-separated)")
@click.option("--output", "-o", default="honeypot.log", help="Log file for connections")
def cmd(ports, output):
    """Opens fake local services and logs connecting IP addresses."""
    port_list = [int(p.strip()) for p in ports.split(",")]
    
    console.print(f"[bold cyan]Starting Local Honeypot...[/bold cyan]")
    console.print(f"[bold cyan]Listening on ports:[/bold cyan] {ports}")
    console.print(f"[bold cyan]Logging to:[/bold cyan] {output}")
    console.print("[yellow]Press Ctrl+C to stop.[/yellow]\n")

    def handle_connection(client_sock, port):
        client_ip = client_sock.getpeername()[0]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] Connection on port {port} from {client_ip}\n"
        
        console.print(f"[bold red]ALARM:[/bold red] {log_entry.strip()}")
        
        with open(output, "a") as f:
            f.write(log_entry)
        
        # Send a generic banner
        try:
            if port == 21:
                client_sock.send(b"220 FTP Server Ready\r\n")
            elif port == 22:
                client_sock.send(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n")
            elif port == 80:
                client_sock.send(b"HTTP/1.1 200 OK\r\nServer: Apache/2.4.41\r\n\r\n")
            else:
                client_sock.send(b"Access Denied\r\n")
        except:
            pass
        finally:
            client_sock.close()

    def start_listener(port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind(("0.0.0.0", port))
            server.listen(5)
            while True:
                client, addr = server.accept()
                threading.Thread(target=handle_connection, args=(client, port)).start()
        except Exception as e:
            console.print(f"[bold red]Error on port {port}:[/bold red] {e}")

    threads = []
    for port in port_list:
        t = threading.Thread(target=start_listener, args=(port,), daemon=True)
        t.start()
        threads.append(t)

    try:
        # Keep main thread alive
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[bold green]Honeypot stopped.[/bold green]")
