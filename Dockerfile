FROM mudesrl/camajora-backend:1.6


RUN pip3 install kafka-python

COPY ./odoo/scripts /mnt/utils/scripts
COPY ./odoo/conf /mnt/utils/scripts/conf
# COPY ./odoo/wait-for-it.sh /wait-for-it.sh

COPY ./community-addons/ /mnt/bundle-addons/
COPY ./addons/ /mnt/bundle-addons/

COPY ./odoo/conf/web/nginx.conf /etc/nginx/nginx.conf
COPY ./odoo/conf/web/odoo.conf /etc/nginx/conf.d/default.conf


COPY ./odoo/entrypoint.sh /entrypoint.sh


# CMD ["run"]
#ENTRYPOINT ["/entrypoint.sh"]
CMD ["run"]



