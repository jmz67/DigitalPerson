

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
import app.models.patient as models
import app.schemas.patient as schemas

router = APIRouter(prefix="/v2")

# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/patientInfo")
def get_patient_info():
    return {
        "id": 1234562,
        "name": "王安宇",
        "age": 39,
        "department": "皮肤科"    
    }

@router.get("/patientDetail/{opc_id}", response_model=schemas.ResponseModel)
def get_patient_data(opc_id: str, db: Session = Depends(get_db)):
    # 查询患者数据
    patient = db.query(models.PatientData).filter(models.PatientData.opc_id == opc_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # 构建响应数据
    response_data = schemas.Data(
        patientIdentity=schemas.PatientIdentity(
            patientId=patient.patient_id,
            idType=patient.id_type,
            idNumber=patient.id_number
        ),
        latestMedicalRecord=schemas.LatestMedicalRecord(
            basicInfo=schemas.BasicInfo(
                gender=patient.gender,
                birthday=patient.birthday,
                aboBloodType=patient.abo_blood_type,
                rhBloodType=patient.rh_blood_type
            ),
            vitalSigns=schemas.VitalSigns(
                systolicPressure=patient.systolic_pressure,
                diastolicPressure=patient.diastolic_pressure,
                height=patient.height,
                weight=patient.weight
            ),
            marriageChildInfo=schemas.MarriageChildInfo(
                marriageStatus=patient.marriage_status,
                fullTermCount=patient.full_term_count,
                prematureCount=patient.premature_count,
                abortionCount=patient.abortion_count,
                livingChildrenCount=patient.living_children_count
            ),
            pastHistory=schemas.PastHistory(
                personalHistory=patient.personal_history,
                bloodTransfusionHistory=patient.blood_transfusion_history,
                diseaseHistory=patient.disease_history,
                epidemiologicalHistory=patient.epidemiological_history,
                menstrualHistory=schemas.MenstrualHistory(
                    menarcheAge=patient.menarche_age,
                    intervalDays=patient.interval_days,
                    durationDays=patient.duration_days,
                    isSterilization=patient.is_sterilization,
                    lastMenstrualDate=patient.last_menstrual_date
                ),
                surgeryHistory=patient.surgery_history,
                familyHistory=patient.family_history
            ),
            allergyHistory=patient.allergy_history,
            childGrowthInfo=patient.child_growth_info
        ),
        revisitInfo=schemas.RevisitInfo(
            isRevisit=patient.is_revisit,
            lastRecord=schemas.LastRecord(
                chiefComplaint=patient.chief_complaint,
                presentIllness=patient.present_illness,
                menstrualHistory=schemas.MenstrualHistory(
                    menarcheAge=patient.menarche_age,
                    intervalDays=patient.interval_days,
                    durationDays=patient.duration_days,
                    isSterilization=patient.is_sterilization,
                    lastMenstrualDate=patient.last_menstrual_date
                ),
                tcmFourExams=schemas.TcmFourExams(
                    inspection=patient.inspection,
                    inquiry=patient.inquiry,
                    listeningAndSmelling=patient.listening_and_smelling,
                    palpation=patient.palpation
                ),
                physicalExam=patient.physical_exam,
                auxiliaryExam=patient.auxiliary_exam,
                diagnosis=schemas.Diagnosis(
                    tcmDiagnosisName=patient.tcm_diagnosis_name,
                    tcmDiagnosisCode=patient.tcm_diagnosis_code,
                    tcmSyndromeName=patient.tcm_syndrome_name,
                    westernDiagnosisName=patient.western_diagnosis_name,
                    westernDiagnosisCode=patient.western_diagnosis_code
                ),
                treatmentPrinciple=patient.treatment_principle,
                treatmentAdvice=patient.treatment_advice,
                prescription=schemas.Prescription(
                    prescriptionName=patient.prescription_name,
                    herbs=patient.herbs.split(",") if patient.herbs else []
                )
            )
        )
    )

    return schemas.ResponseModel(
        code=200,
        message="成功",
        data=response_data
    )
