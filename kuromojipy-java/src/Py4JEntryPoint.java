import py4j.GatewayServer;

public class Py4JEntryPoint {
  public static void main(String[] args) {
    Py4JEntryPoint app = new Py4JEntryPoint();
    GatewayServer server = new GatewayServer(app);
    server.start();
  }
}