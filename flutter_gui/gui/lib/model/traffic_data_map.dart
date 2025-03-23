class TrafficDataMap {
  final int trafficLightId;
  final String phaseId;
  final double cycleTime;
  final double greenTime;
  final double lostTime;
  final String lightState;
  //final String phaseId;

  TrafficDataMap(
    this.trafficLightId,
    this.phaseId,
    this.cycleTime,
    this.greenTime,
    this.lostTime,
    this.lightState,
  );

  TrafficDataMap.fromJson(Map<String, dynamic> json)
    : trafficLightId = json['traffic_light_id'] as int,
      phaseId = json['phase_id'] as String,
      cycleTime = json['cycle_time'] as double,
      greenTime = json['green_time'] as double,
      lostTime = json['lost_time'] as double,
      lightState = json['light_state'] as String;
}
