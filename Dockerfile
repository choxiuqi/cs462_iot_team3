FROM python:3.6
WORKDIR /usr/src/app
COPY req.txt ./
RUN pip install --no-cache-dir -r req.txt
COPY . /
CMD ["python", "/Function_Scripts/getevents.py"]