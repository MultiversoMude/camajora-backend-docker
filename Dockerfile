FROM metadonors/odoo:12.0

ENV BUNDLES_PATH /mnt/bundle-addons

COPY requirements.txt /mnt/utils/extra-requirements.txt

RUN pip3 install -r /mnt/utils/extra-requirements.txt

COPY ./conf/default-site.conf /etc/nginx/conf.d/default.conf
COPY conf/odoo_conf.yaml /mnt/utils/scripts/conf/odoo_conf.yaml

COPY ./addons/ /mnt/bundle-addons/

RUN chown -R odoo.odoo /mnt/bundle-addons/camajora-addons

CMD ["run"]



