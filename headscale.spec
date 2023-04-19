# Generated by go2rpm 1.9.0
%bcond_without check
# pull in deps dynamically from the web
%global gomodulesmode GO111MODULE=on

# https://github.com/juanfont/headscale
%global goipath         github.com/juanfont/headscale
Version:                0.21.0

%if 0%{?rhel}
%gometa
%else
%gometa -f
%endif


%global common_description %{expand:
An open source, self-hosted implementation of the Tailscale control server.}

%global golicenses      LICENSE

Name:           headscale
Release:        1
Summary:        An open source, self-hosted implementation of the Tailscale control server

License:        BSD-3-Clause
URL:            %{gourl}
Source0:        https://github.com/juanfont/headscale/archive/v%{version}/headscale-%{version}.tar.gz
Source1:        headscale.service
Source2:        headscale.tmpfiles
Source3:        headscale.sysusers
Source4:        config.yaml

BuildRequires:  git-core
BuildRequires:  systemd-rpm-macros
%if 0%{?rhel}
BuildRequires:  wget
%endif

%description %{common_description}


%gopkg


%prep
%goprep
%autopatch -p1

# we don't need to build this
rm -rf cmd/gh-action-integration-generator

#%%generate_buildrequires
#%%go_generate_buildrequires


%build
export GOFLAGS=-modcacherw

for cmd in cmd/* ; do
  %gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done


%install
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -d -m 0755 %{buildroot}/run/%{name}/
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/headscale.sysusers
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -p -d -m 0755 %{buildroot}%{_sharedstatedir}/headscale/
install -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/headscale/config.yaml


%if %{with check}
#%%check
#%%gocheck
%endif


%pre
%sysusers_create_compat %{SOURCE3}


%post
%systemd_post headscale.service


%preun
%systemd_preun headscale.service


%postun
%systemd_postun_with_restart headscale.service


%files
%license LICENSE
%doc docs/ README.md CHANGELOG.md
%{_bindir}/headscale
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.sysusers
%{_unitdir}/%{name}.service
%dir %attr(0755,headscale,headscale) %{_sharedstatedir}/%{name}/
%attr(0755,headscale,headscale) %{_sysconfdir}/%{name}/
%attr(0644,headscale,headscale) %config(noreplace) %{_sysconfdir}/%{name}/config.yaml

%gopkgfiles


%changelog
* Wed Apr 19 2023 Jonathan Wright <jonathan@almalinux.org> - 0.21.0-1
- Initial package build
