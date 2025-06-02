-- Global Solution - 1/2025 - POC
-- Estrutura de dados

DROP TABLE T_4E_017_ITAICI_RIVER_HISTORY CASCADE CONSTRAINTS;

-- Criação de tableas

CREATE TABLE T_4E_017_ITAICI_RIVER_HISTORY (
    reading_id NUMBER(5) NOT NULL,
    reading_timestamp DATE NOT NULL,
    reading_water_level NUMBER (5, 2),
    flag_flood BOOLEAN,
    reading_calculated_water_pressure NUMBER (6, 2),
    flag_overcharge BOOLEAN
);

CREATE TABLE T_4E_017_AJD_BRIDGE_METADATA (
    bridge_id NUMBER(3) NOT NULL,
    bridge_main_material VARCHAR(30),
    bridge_charge_rupture_limit NUMBER(6, 2),
    bridge_safety_factor NUMBER(2, 1)
);

CREATE TABLE T_4E_047_AJD_BRIDGE_HISTORY (
    event_id NUMBER(3) NOT NULL,
    event_timestamp DATE NOT NULL,
    event_type VARCHAR(30),
    event_description VARCHAR(256),
    event_severity NUMBER(2) 
)