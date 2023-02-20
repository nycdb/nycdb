ALTER TABLE dof_tax_lien_sale_list ADD COLUMN reportdate DATE;
UPDATE dof_tax_lien_sale_list SET reportdate = TO_DATE('01/' || month, 'DD/MM/YYY');
ALTER TABLE dof_tax_lien_sale_list DROP COLUMN month;

CREATE INDEX dof_tax_lien_sale_list_bbl_idx on dof_tax_lien_sale_list (bbl);
