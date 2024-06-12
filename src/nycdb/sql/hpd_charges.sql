CREATE INDEX hpd_omo_invoices_invoiceid_idx ON hpd_omo_invoices (invoiceid);

CREATE INDEX hpd_omo_charges_omoid_idx ON hpd_omo_charges (omoid);
CREATE INDEX hpd_omo_charges_bbl_idx ON hpd_omo_charges (bbl);

CREATE INDEX hpd_hwo_charges_bbl_idx ON hpd_hwo_charges (bbl);

CREATE INDEX hpd_fee_charges_bbl_idx ON hpd_fee_charges (bbl);
CREATE INDEX hpd_fee_charges_feeid_idx ON hpd_fee_charges (feeid);
CREATE INDEX hpd_fee_charges_feeissueddate_idx ON hpd_fee_charges (feeissueddate);
