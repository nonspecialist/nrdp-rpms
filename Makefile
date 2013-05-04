SPEC=nrdp.spec
SOURCE=nrdp.zip
SRCDIR := $(shell /usr/bin/rpmbuild --eval '%{_sourcedir}' 2>/dev/null)
SRCS=$(SRCDIR)/$(SOURCE)
BASE=http://assets.nagios.com/downloads/nrdp

.DEFAULT: all

all: $(SRCS) srpm rpm

$(SRCS):
	wget -O $(SRCDIR)/$(SOURCE) $(BASE)/$(SOURCE)
	cp *.patch $(SRCDIR)

srpm:
	rpmbuild -bs $(SPEC)

rpm:
	rpmbuild -bb $(SPEC)
