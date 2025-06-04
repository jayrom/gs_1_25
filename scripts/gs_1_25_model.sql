-- Global Solution - 1/2025 - POC
-- Estrutura de dados

-- Limpeza inicial

DROP TABLE T_4E_047_ITAICI_RIVER_HISTORY CASCADE CONSTRAINTS;
DROP TABLE T_4E_047_EQUIP_METADATA CASCADE CONSTRAINTS;
DROP TABLE T_4E_047_EQUIP_HISTORY CASCADE CONSTRAINTS;

-- Criação de tableas

-- Histórico de leituras do nível do rio Itaici
CREATE TABLE T_4E_047_ITAICI_RIVER_HISTORY (
    reading_id NUMBER(5) NOT NULL,
    reading_timestamp DATE NOT NULL,
    reading_water_level NUMBER (5, 2),
    flag_flood NUMBER(1) DEFAULT 0 NOT NULL,
    reading_calculated_water_pressure NUMBER (6, 2),
         NUMBER(1) DEFAULT 0 NOT NULL
);

ALTER TABLE T_4E_047_ITAICI_RIVER_HISTORY
    ADD CONSTRAINT PK_T_4E_047_ITAICI_RIVER_HISTORY PRIMARY KEY (reading_id);
CREATE SEQUENCE SEQ_T_4E_047_ITAICI_RIVER_HISTORY START WITH 1 INCREMENT BY 1;

-- Metadados de equipamentos
CREATE TABLE T_4E_047_EQUIP_METADATA (
    equip_id NUMBER(3) NOT NULL,
    equip_main_material VARCHAR(30),
    equip_charge_rupture_limit NUMBER(6, 2),
    equip_safety_factor NUMBER(2, 1)
);

ALTER TABLE T_4E_047_EQUIP_METADATA
    ADD CONSTRAINT PK_T_4E_047_EQUIP_METADATA PRIMARY KEY (equip_id);
CREATE SEQUENCE SEQ_T_4E_047_EQUIP_METADATA START WITH 1 INCREMENT BY 1;

-- Histórico de eventos de equipamentos
-- Pode incluir manutenção, inspeções, danos etc.
CREATE TABLE T_4E_047_EQUIP_HISTORY (
    event_id NUMBER(3) NOT NULL,
    equip_id NUMBER(3) NOT NULL,
    event_timestamp DATE NOT NULL,
    event_type VARCHAR(30),
    event_description VARCHAR(256),
    event_severity NUMBER(2) 
);

ALTER TABLE T_4E_047_EQUIP_HISTORY 
    ADD CONSTRAINT PK_T_4E_047_EQUIP_HISTORY PRIMARY KEY (event_id);
CREATE SEQUENCE SEQ_T_4E_047_EQUIP_HISTORY START WITH 1 INCREMENT BY 1;

commit;