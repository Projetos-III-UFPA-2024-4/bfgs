class TrafficLight {
  int? id;
  String? state;

  trafficLightMap() {
    var mapping = <String, dynamic>{};
    mapping['id'] = id;
    mapping['state'] = state!;

    return mapping;
  }
}