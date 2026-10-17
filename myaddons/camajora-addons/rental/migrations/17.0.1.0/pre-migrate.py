def migrate(cr, version):
    cr.execute('ALTER TABLE public.rental_availability ADD COLUMN IF NOT EXISTS  starthour float8 ')
    cr.execute('ALTER TABLE public.rental_availability ADD COLUMN IF NOT EXISTS  endhour  float8 ')
    cr.execute('ALTER TABLE public.rental_booking_slot ALTER COLUMN  start_time TYPE float8')
    cr.execute('ALTER TABLE public.rental_booking_slot ALTER COLUMN  end_time TYPE float8')
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS latitudo float8 NULL')
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS longitudo float8 NULL')
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS  contact_email_ref varchar NULL DEFAULT '
               '\'To insert\'')
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS '
               'contact_mobile_ref varchar NULL DEFAULT \'To '
               'insert\'::character varying')
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS'
               ' contact_name_ref varchar NULL DEFAULT \'To insert\'::character '
               'varying')
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS '
               'hotspot_name varchar NULL DEFAULT \'To insert\'::character '
               'varying;')
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS '
               'scc_address varchar NULL DEFAULT \'To insert\'::character '
               'varying')
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS '
               'ip_device_door_opening varchar NULL DEFAULT \'To insert\'::character varying(15);')
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS opened_from float8 null')
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS opened_to   float8 null')
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS '
               'scc_endpoint_open_door varchar NULL DEFAULT \'To insert\'::character '
               'varying')
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS '
               'scc_endpoint_open_door_protocol varchar(15) NULL DEFAULT \'To insert\'::character '
               'varying')
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS '
               'scc_endpoint_open_door_port varchar(10) NULL DEFAULT \'To insert\'::character '
               'varying')
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS '
               'scc_endpoint_resource_activation varchar(150) NULL DEFAULT \'To insert\'::character '
               'varying')
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS '
               'scc_endpoint_resource_activation_protocol varchar(5) NOT NULL DEFAULT \'http\'::character '
               'varying')
    cr.execute('ALTER TABLE public.rental_location ADD COLUMN IF NOT EXISTS '
               'scc_endpoint_resource_activation_port varchar(15) NOT NULL DEFAULT \'8080\'::character '
               'varying')
    cr.execute('ALTER TABLE public.rental_resource ADD COLUMN IF NOT EXISTS '
               'door_present bool NULL  DEFAULT false')
    cr.execute('ALTER TABLE public.rental_resource ADD COLUMN IF NOT EXISTS '
               ' modbus_group int4 NULL')
    cr.execute('ALTER TABLE public.rental_resource ADD COLUMN IF NOT EXISTS '
               ' modbus_id int4 NULL')
    cr.execute('ALTER TABLE public.rental_resource ADD COLUMN IF NOT EXISTS'
               ' modbus_plugin varchar NULL')
    cr.execute('ALTER TABLE public.rental_resource ADD COLUMN IF NOT EXISTS'
               ' api_url varchar NULL')
    cr.execute('ALTER TABLE public.rental_resource ADD COLUMN IF NOT EXISTS'
               ' api_key varchar NULL')
    cr.execute('ALTER TABLE public.rental_resource ADD COLUMN IF NOT EXISTS'
               ' api_path varchar NULL')
    cr.execute('ALTER TABLE public.rental_resource ADD COLUMN IF NOT EXISTS'
               ' plugin_type varchar NULL')



