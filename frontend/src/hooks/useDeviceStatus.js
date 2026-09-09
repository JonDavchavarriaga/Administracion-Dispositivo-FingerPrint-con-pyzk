import { useEffect, useRef } from "react";

export function useDeviceStatus(onEvent) {
  const callbackRef = useRef(onEvent);

  useEffect(() => {
    callbackRef.current = onEvent;
  }, [onEvent]);

  useEffect(() => {
    const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
    const websocketUrl = apiUrl.replace(/^http/, "ws") + "/ws/devices";
    let socket;
    let reconnectTimer;
    let stopped = false;

    function connect() {
      socket = new WebSocket(websocketUrl);
      socket.onmessage = (event) => callbackRef.current(JSON.parse(event.data));
      socket.onclose = () => {
        if (!stopped) reconnectTimer = setTimeout(connect, 2000);
      };
    }

    connect();
    return () => {
      stopped = true;
      clearTimeout(reconnectTimer);
      socket?.close();
    };
  }, []);
}
