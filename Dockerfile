FROM python:3
WORKDIR /usr/src/app
COPY ../req.txt ./
RUN pip install --no-cache-dir -r ../req.txt
COPY Sub_3.py .
CMD [ "python", "Sub_3.py" ]
