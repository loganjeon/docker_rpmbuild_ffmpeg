FROM centos:centos7.2.1511

MAINTAINER 0.1 yg.jeon@sk.com

RUN yum install -y git wget gcc make yum-plugin-ovl
RUN yum install -y rpm-build
RUN yum install -y epel-release; yum clean all
RUN yum install -y yasm 

RUN useradd -ms /bin/bash devuser
USER devuser
WORKDIR /home/devuser/

RUN mkdir -p /home/devuser/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
ADD ffmpeg.spec /home/devuser/rpmbuild/SPECS/
RUN cd /home/devuser/rpmbuild/SOURCES
RUN wget -q http://ffmpeg.org/releases/ffmpeg-4.0.1.tar.gz -O /home/devuser/rpmbuild/SOURCES/ffmpeg-4.0.1.tar.gz
RUN cd /home/devuser/rpmbuild/SPECS/
RUN rpmbuild -bb /home/devuser/rpmbuild/SPECS/ffmpeg.spec


