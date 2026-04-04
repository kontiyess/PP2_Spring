CREATE OR REPLACE PROCEDURE insert_or_update(name TEXT, phone TEXT)
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE phonebook.name = insert_or_update.name) THEN
        UPDATE phonebook
        SET phone = insert_or_update.phone
        WHERE phonebook.name = insert_or_update.name;
    ELSE
        INSERT INTO phonebook(name, phone)
        VALUES (insert_or_update.name, insert_or_update.phone);
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE delete_contact(value TEXT)
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = value OR phone = value;
END;
$$ LANGUAGE plpgsql;