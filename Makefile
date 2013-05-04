SPEC=nrdp.spec
SOURCE=nrdp.zip
BASE=http://assets.nagios.com/downloads/nrdp

.DEFAULT: all

all: $(SOURCE) srpm rpm

$(SOURCE):
	wget $(BASE)/$(SOURCE)

srpm:
	rpmbuild -bs $(SPEC)

rpm:
	rpmbuild -bb $(SPEC)

clean:
	rm -f $(SOURCE)
