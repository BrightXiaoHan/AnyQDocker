FROM keejo/anyq:1.0 as builder

ENV ANYQ_HOME=/home/AnyQ
ADD . /home/faq
WORKDIR /home/faq
RUN bash deploy/prepare.sh

VOLUME /home/AnyQ/build/solr-4.10.3-anyq/example/solr/collection1

EXPOSE 8080
CMD ["bash", "deploy/run.sh"]