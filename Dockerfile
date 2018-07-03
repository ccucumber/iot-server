FROM python
COPY . /usr/src/mpp
WORKDIR /usr/src/mpp
RUN pip install -r requirements.txt
EXPOSE 81,8086

CMD ["python", "main.py"]
