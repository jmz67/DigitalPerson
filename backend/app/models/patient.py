from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class PatientData(Base):
    __tablename__ = "patient_data"

    opc_id = Column(String(256), primary_key=True, index=True)
    patient_id = Column(String(256), index=True)
    id_type = Column(String(256))
    id_number = Column(String(256))

    # Basic Info
    gender = Column(String(256))
    birthday = Column(Date)
    abo_blood_type = Column(String(256))
    rh_blood_type = Column(String(256))

    # Vital Signs
    systolic_pressure = Column(Integer)
    diastolic_pressure = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)

    # Marriage and Child Info
    marriage_status = Column(String(256))
    full_term_count = Column(Integer)
    premature_count = Column(Integer)
    abortion_count = Column(Integer)
    living_children_count = Column(Integer)

    # Past History
    personal_history = Column(String(256))
    blood_transfusion_history = Column(String(256))
    disease_history = Column(String(256))
    epidemiological_history = Column(String(256))
    menarche_age = Column(Integer)
    interval_days = Column(Integer)
    duration_days = Column(Integer)
    is_sterilization = Column(Boolean)
    last_menstrual_date = Column(Date)
    surgery_history = Column(String(256))
    family_history = Column(String(256))

    # Allergy and Child Growth Info
    allergy_history = Column(String(256))
    child_growth_info = Column(String(256), nullable=True)

    # Revisit Info
    is_revisit = Column(Boolean, default=False)
    chief_complaint = Column(String(256))
    present_illness = Column(String(256))
    inspection = Column(String(256))
    inquiry = Column(String(256))
    listening_and_smelling = Column(String(256))
    palpation = Column(String(256))
    physical_exam = Column(String(256))
    auxiliary_exam = Column(String(256))
    tcm_diagnosis_name = Column(String(256))
    tcm_diagnosis_code = Column(String(256))
    tcm_syndrome_name = Column(String(256))
    western_diagnosis_name = Column(String(256))
    western_diagnosis_code = Column(String(256))
    treatment_principle = Column(String(256))
    treatment_advice = Column(String(256))
    prescription_name = Column(String(256))
    herbs = Column(String(256))  # 存储为逗号分隔的字符串
