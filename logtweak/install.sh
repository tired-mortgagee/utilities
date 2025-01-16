#!/bin/sh

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

mkdir /opt/logtweak
cp *.ini /opt/logtweak
cp *.py /opt/logtweak
chown root:root /opt/logtweak/*
chomd 755 /opt/logtweak/*.py
chmod 644 /opt/logtweak/*.ini

if [ -f /etc/systemd/system/logtweak.service ]; then
  rm -f /etc/systemd/system/logtweak.service
fi
tee -a /etc/systemd/system/logtweak.service > /dev/null <<EOT
[Unit]
Description=Logtweak service
After=network.target

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
Group=root
WorkingDirectory=/opt/logtweak
ExecStart=/opt/logtweak/logtweak.py

[Install]
WantedBy=multi-user.target
EOT

systemctl daemon-reload
systemctl enable logtweak.service
systemctl start logtweak.service
