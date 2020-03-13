FROM python:3
WORKDIR /cs462_iot_team3/Function_Scripts
COPY req.txt ./
RUN pip install --no-cache-dir -r req.txt
COPY ./Function_Scripts/Sub_3.py .
CMD [ "python", "./Function_Scripts/Sub_3.py" ]
