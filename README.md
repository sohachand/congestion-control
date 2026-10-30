# Congestion Control: TCP Window, Leaky Bucket and Token Bucket

Mini-project by Soha Chand.

- `simulator/index.html`: single-file interactive simulator (open in a browser). Tabs: TCP Window, Leaky Bucket, Token Bucket, Congestion Demo (control OFF vs ON, optional shaper).
- `presentation/`: 24-slide PowerPoint.
- `report/`: project synopsis (Word).
- `packet-tracer/Congestion_Control_Lab.pkt`: Cisco Packet Tracer lab (two LANs over a WAN link, QoS `shape average 128000` policy configured but not bound, since binding it blocks traffic in Packet Tracer).
- `scripts/make_figures.py`: matplotlib script for the report figures.
- `screenshots/`: Congestion Demo screenshots.

The simulator is a simplified model; TCP-tab packet loss is simulated.
