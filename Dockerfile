FROM python:3.7-stretch
MAINTAINER Igor Kozyrenko <igor@ikseek.com>
RUN apt-get update && apt-get install -y --no-install-recommends \
		dnsmasq \
	&& rm -rf /var/lib/apt/lists/* \
	&& pip install pipenv
WORKDIR /app/
COPY Pipfile* ./
RUN pipenv install --deploy --system
COPY acuhack acuhack
ENTRYPOINT [ "python", "-m", "acuhack"]
