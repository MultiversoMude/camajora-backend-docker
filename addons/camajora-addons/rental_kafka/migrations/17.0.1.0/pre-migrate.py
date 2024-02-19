def migrate(cr, version):
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS kafka_configuration int4 null')
