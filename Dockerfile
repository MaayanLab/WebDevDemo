FROM debian:stable

RUN set -x \
  && echo "Preparing user..." \
  && useradd -ms /bin/bash -d /app app

ADD deps.txt /app/deps.txt
RUN set -x \
  && echo "Installing system dependencies from deps.txt..." \
  && apt-get -y update \
  && apt-get -y install $(grep -v '^#' /app/deps.txt) \
  && rm /app/deps.txt

ADD requirements.txt /app/requirements.txt
RUN set -x \
  && echo "Installing python dependencies from requirements.txt..." \
  && pip3 install -Ivr /app/requirements.txt \
  && rm /app/requirements.txt

EXPOSE 80
ADD boot.sh /app/boot.sh
RUN set -x && chmod +x /app/boot.sh
CMD /app/boot.sh

ADD app /app/app
RUN set -x && chown app:app -R /app/

ADD init_db.py /app/init_db.py
ADD fill_db.py /app/fill_db.py
ADD data/enriched_terms.tsv /app/data/enriched_terms.tsv


RUN python3 /app/init_db.py
RUN python3 /app/fill_db.py /app/data/enriched_terms.tsv