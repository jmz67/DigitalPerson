from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class PatientIdentity(BaseModel):
    patientId: Optional[str] = None
    idType: Optional[str] = None
    idNumber: Optional[str] = None

class BasicInfo(BaseModel):
    gender: Optional[str] = None
    birthday: Optional[date] = None
    aboBloodType: Optional[str] = None
    rhBloodType: Optional[str] = None

class VitalSigns(BaseModel):
    systolicPressure: Optional[int] = None
    diastolicPressure: Optional[int] = None
    height: Optional[int] = None
    weight: Optional[int] = None

class MarriageChildInfo(BaseModel):
    marriageStatus: Optional[str] = None
    fullTermCount: Optional[int] = None
    prematureCount: Optional[int] = None
    abortionCount: Optional[int] = None
    livingChildrenCount: Optional[int] = None

class MenstrualHistory(BaseModel):
    menarcheAge: Optional[int] = None
    intervalDays: Optional[int] = None
    durationDays: Optional[int] = None
    isSterilization: Optional[bool] = None
    lastMenstrualDate: Optional[date] = None

class PastHistory(BaseModel):
    personalHistory: Optional[str] = None
    bloodTransfusionHistory: Optional[str] = None
    diseaseHistory: Optional[str] = None
    epidemiologicalHistory: Optional[str] = None
    menstrualHistory: Optional[MenstrualHistory] = None
    surgeryHistory: Optional[str] = None
    familyHistory: Optional[str] = None

class LatestMedicalRecord(BaseModel):
    basicInfo: Optional[BasicInfo] = None
    vitalSigns: Optional[VitalSigns] = None
    marriageChildInfo: Optional[MarriageChildInfo] = None
    pastHistory: Optional[PastHistory] = None
    allergyHistory: Optional[str] = None
    childGrowthInfo: Optional[str] = None

class Diagnosis(BaseModel):
    tcmDiagnosisName: Optional[str] = None
    tcmDiagnosisCode: Optional[str] = None
    tcmSyndromeName: Optional[str] = None
    westernDiagnosisName: Optional[str] = None
    westernDiagnosisCode: Optional[str] = None

class Prescription(BaseModel):
    prescriptionName: Optional[str] = None
    herbs: Optional[List[str]] = None

class TcmFourExams(BaseModel):
    inspection: Optional[str] = None
    inquiry: Optional[str] = None
    listeningAndSmelling: Optional[str] = None
    palpation: Optional[str] = None

class LastRecord(BaseModel):
    chiefComplaint: Optional[str] = None
    presentIllness: Optional[str] = None
    menstrualHistory: Optional[MenstrualHistory] = None
    tcmFourExams: Optional[TcmFourExams] = None
    physicalExam: Optional[str] = None
    auxiliaryExam: Optional[str] = None
    diagnosis: Optional[Diagnosis] = None
    treatmentPrinciple: Optional[str] = None
    treatmentAdvice: Optional[str] = None
    prescription: Optional[Prescription] = None

class RevisitInfo(BaseModel):
    isRevisit: Optional[bool] = None
    lastRecord: Optional[LastRecord] = None

class Data(BaseModel):
    patientIdentity: Optional[PatientIdentity] = None
    latestMedicalRecord: Optional[LatestMedicalRecord] = None
    revisitInfo: Optional[RevisitInfo] = None

class ResponseModel(BaseModel):
    code: Optional[int] = None
    message: Optional[str] = None
    data: Optional[Data] = None
