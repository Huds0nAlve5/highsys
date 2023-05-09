CREATE TABLE IF NOT EXISTS usuario(
    usrcod INT(4) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT,
    usrnome CHAR(15) UNIQUE NOT NULL,
    usrsen CHAR(64) NOT NULL,
    PRIMARY KEY(usrcod) 
);

CREATE TABLE IF NOT EXISTS produto(
    procod INT(9) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT,
    prodes CHAR(60) NOT NULL,
    prosec INT(2) UNSIGNED ZEROFILL NOT NULL,
    procodbrr INT(13),
    proprc NUMERIC(7, 2) NOT NULL,
    protrib CHAR(3) NOT NULL,
    proncm INT(8) NOT NULL,
    proimg CHAR(70),
    PRIMARY KEY(procod) 
);

CREATE TABLE IF NOT EXISTS secao(
    seccod INT(2) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT,
    secdes CHAR(50) NOT NULL,
    PRIMARY KEY(seccod)
);

CREATE TABLE IF NOT EXISTS tributacao(
    tribcod CHAR(3) NOT NULL,
    PRIMARY KEY(tribcod)
);

CREATE TABLE IF NOT EXISTS ncm(
    ncm INT(8) NOT NULL,
    PRIMARY KEY(ncm)
);

CREATE TABLE IF NOT EXISTS estoque(
    procod INT(9) UNSIGNED ZEROFILL NOT NULL,
    proest NUMERIC(10,2),
    PRIMARY KEY(procod)
);

ALTER TABLE produto ADD FOREIGN KEY (prosec)REFERENCES secao(seccod);
ALTER TABLE produto ADD FOREIGN KEY (protrib)REFERENCES tributacao(tribcod);
ALTER TABLE produto ADD FOREIGN KEY (proncm)REFERENCES ncm(ncm);
ALTER TABLE estoque ADD FOREIGN KEY (procod)REFERENCES produto(procod);

INSERT INTO tributacao VALUES("F00");
INSERT INTO tributacao VALUES("T18");
INSERT INTO tributacao VALUES("I00");
INSERT INTO tributacao VALUES("N00");
INSERT INTO ncm VALUES("00000000");
INSERT INTO ncm VALUES("11111111");
INSERT INTO ncm VALUES("22222222");
INSERT INTO ncm VALUES("33333333");

create trigger iniciar_estoque
after insert
on produto
for each row
	insert into estoque values(new.procod, 0);

CREATE TRIGGER exclusao_produto BEFORE DELETE ON produto
FOR EACH ROW
    DELETE FROM estoque WHERE procod = OLD.procod;


INSERT INTO usuario VALUES(1, "hudsonalves", "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4")