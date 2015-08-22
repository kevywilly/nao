

from naoqi import ALProxy

diagnosis = ALProxy("ALDiagnosis", "192.168.1.117", 9559)

report = diagnosis.getActiveDiagnosis()

print diagnosis.getActiveDiagnosis()

print diagnosis.getPassiveDiagnosis()