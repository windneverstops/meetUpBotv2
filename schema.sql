CREATE TABLE guild (
    guild_id VARCHAR(25) NOT NULL COMMENT 'guild identifier',
    guild_bot_admin_id VARCHAR(20) NOT NULL COMMENT 'bot admin\'discord id'
);

Alter table guild add constraint guild_pk PRIMARY KEY (guild_id);

CREATE TABLE meet_up (
    guild_id VARCHAR(25) NOT NULL COMMENT 'guild identifier',
    mu_creator_id VARCHAR(20) NOT NULL COMMENT 'meet up creator\'s discord id',
    mu_name VARCHAR(200) NOT NULL COMMENT 'name of the meet up. Also identifier',
    mu_startdate DATETIME COMMENT 'start date of the meet up',
    mu_enddate DATETIME COMMENT 'end date of the meet up',
    mu_description VARCHAR(5000) COMMENT 'description of the meet up',
    mu_location VARCHAR(200) COMMENT 'location of the meet up',
    mu_status VARCHAR(200) COMMENT 'status of the meet up',
    mu_payamount NUMERIC(8 , 2 ) COMMENT 'monies to be paid',
    mu_payto VARCHAR(5000) COMMENT 'person whom monies is owed to',
    mu_payinfo VARCHAR(5000) COMMENT 'Other/alternative payment information',
    mu_other VARCHAR(5000) COMMENT 'other information pertaining to meet up'
);

alter table meet_up add constraint mu_pk primary key (mu_name);
alter table meet_up add constraint mu_fk foreign key (guild_id) REFERENCES guild(guild_id);



