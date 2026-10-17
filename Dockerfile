FROM odoo:17.0

USER root
#RUN cat /etc/apt/sources.list
#RUN sed -i 's/stable\/updates/stable-security\/updates/' /etc/apt/sources.list
RUN mkdir -p /var/lib/odoo/sessions && chown -R odoo:odoo /var/lib/odoo/sessions
RUN mkdir -p /mnt/utils /mnt/bundle-addons \
    && chown -R odoo:odoo /mnt/utils /mnt/bundle-addons

RUN apt-get update \
    && apt-get install -y  \
        vim \
        libtool \
        nginx \
        sudo \
        pkg-config \
        python3-dev \
        libffi-dev \
        python3 \
		#python3.8-dev  \
        #python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY ./odoo/extra-requirements.txt /mnt/utils/extra-requirements.txt
RUN export PIP_DEFAULT_TIMEOUT=1000000
RUN pip3 install -U wheel setuptools==58.0.0
RUN pip3 install -r /mnt/utils/extra-requirements.txt

COPY ./odoo/scripts /mnt/utils/scripts
COPY ./odoo/conf /mnt/utils/scripts/conf
# COPY ./odoo/wait-for-it.sh /wait-for-it.sh

COPY ./community-addons/ /mnt/bundle-addons/
COPY ./addons/ /mnt/bundle-addons/

COPY ./odoo/conf/web/nginx.conf /etc/nginx/nginx.conf
COPY ./odoo/conf/web/odoo.conf /etc/nginx/conf.d/default.conf


COPY ./odoo/entrypoint.sh /entrypoint.sh


# CMD ["run"]
ENTRYPOINT ["/entrypoint.sh"]
CMD ["run"]



