ALTER TABLE dof_tax_lien_sale_list ADD COLUMN report_date DATE;
UPDATE dof_tax_lien_sale_list SET report_date = TO_DATE('01/' || month, 'DD/MM/YYY');
ALTER TABLE dof_tax_lien_sale_list DROP COLUMN month;

CREATE INDEX dof_tax_lien_sale_list_bbl_idx on dof_tax_lien_sale_list (bbl);
