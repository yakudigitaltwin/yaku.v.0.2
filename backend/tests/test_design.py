from app.calculations.design import rapid_mix, sedimentation

def test_rapid_mix():
    r = rapid_mix(0.5, 30, 60)
    assert r["detention_time_s"] == 60
    assert r["power_w"] > 0

def test_sedimentation():
    r = sedimentation(0.5, 1500, 4)
    assert r["volume_m3"] == 6000
