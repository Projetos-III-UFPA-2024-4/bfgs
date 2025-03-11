class TrafficLight {
  int? id;
  String? state;

  trafficLightMap() {
    var mapping = Map<String, dynamic>();
    mapping['id'] = id ?? null;
    mapping['state'] = state!;

    return mapping;
  }
}