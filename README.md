<div align="center">
    <a href="https://erpnext.com">
        <img src="https://raw.githubusercontent.com/frappe/erpnext/develop/erpnext/public/images/erpnext-logo.png" height="128">
    </a>
    <h2>ERPNext</h2>
    <div align="center">
        <p>ERP made simple</p>
    </div>

[![CI](https://github.com/frappe/erpnext/actions/workflows/server-tests.yml/badge.svg?branch=develop)](https://github.com/frappe/erpnext/actions/workflows/server-tests.yml)
[![UI](https://github.com/erpnext/erpnext_ui_tests/actions/workflows/ui-tests.yml/badge.svg?branch=develop&event=schedule)](https://github.com/erpnext/erpnext_ui_tests/actions/workflows/ui-tests.yml)
[![Open Source Helpers](https://www.codetriage.com/frappe/erpnext/badges/users.svg)](https://www.codetriage.com/frappe/erpnext)
[![codecov](https://codecov.io/gh/frappe/erpnext/branch/develop/graph/badge.svg?token=0TwvyUg3I5)](https://codecov.io/gh/frappe/erpnext)
[![docker pulls](https://img.shields.io/docker/pulls/frappe/erpnext-worker.svg)](https://hub.docker.com/r/frappe/erpnext-worker)

[https://erpnext.com](https://erpnext.com)

</div>

ERPNext as a monolith includes the following areas for managing businesses:

1. [Accounting](https://erpnext.com/open-source-accounting)
1. [Warehouse Management](https://erpnext.com/distribution/warehouse-management-system)
1. [CRM](https://erpnext.com/open-source-crm)
1. [Sales](https://erpnext.com/open-source-sales-purchase)
1. [Purchase](https://erpnext.com/open-source-sales-purchase)
1. [HRMS](https://erpnext.com/open-source-hrms)
1. [Project Management](https://erpnext.com/open-source-projects)
1. [Support](https://erpnext.com/open-source-help-desk-software)
1. [Asset Management](https://erpnext.com/open-source-asset-management-software)
1. [Quality Management](https://erpnext.com/docs/user/manual/en/quality-management)
1. [Manufacturing](https://erpnext.com/open-source-manufacturing-erp-software)
1. [Website Management](https://erpnext.com/open-source-website-builder-software)
1. [Customize ERPNext](https://erpnext.com/docs/user/manual/en/customize-erpnext)
1. [And More](https://erpnext.com/docs/user/manual/en/)

ERPNext is built on the [Frappe Framework](https://github.com/frappe/frappe), a full-stack web app framework built with Python & JavaScript.

## Installation

<div align="center" style="max-height: 40px;">
    <a href="https://frappecloud.com/erpnext/signup">
        <img src=".github/try-on-f-cloud-button.svg" height="40">
    </a>
    <a href="https://labs.play-with-docker.com/?stack=https://raw.githubusercontent.com/frappe/frappe_docker/main/pwd.yml">
      <img src="https://raw.githubusercontent.com/play-with-docker/stacks/master/assets/images/button.png" alt="Try in PWD" height="37"/>
    </a>
</div>

> Login for the PWD site: (username: Administrator, password: admin)

### Containerized Installation

Use docker to deploy ERPNext in production or for development of [Frappe](https://github.com/frappe/frappe) apps. See https://github.com/frappe/frappe_docker for more details.

### Motivation

Running a business is a complex task - handling invoices, tracking stock, managing personnel, and other daily operations. In a market where software is sold separately to manage each of these tasks, ERPNext does all of the above and more, for free.

### Key Features

- **Accounting**: All the tools you need to manage cash flow in one place, right from recording transactions to summarizing and analyzing financial reports.
- **Order Management**: Track inventory levels, replenish stock, and manage sales orders, customers, suppliers, shipments, deliverables, and order fulfillment.
- **Manufacturing**: Simplifies the production cycle, helps track material consumption, exhibits capacity planning, handles subcontracting, and more!
- **Asset Management**: From purchase to disposal, IT infrastructure to equipment. Covers every branch of your organization, all in one centralized system.
- **Projects**: Deliver both internal and external projects on time, budget and profitability. Track tasks, timesheets, and issues by project.

<details open>

<summary>More</summary>
	<img src="https://erpnext.com/files/v16_bom.png"/>
	<img src="https://erpnext.com/files/v16_stock_summary.png"/>
	<img src="https://erpnext.com/files/v16_job_card.png"/>
	<img src="https://erpnext.com/files/v16_tasks.png"/>
</details>

### Under the Hood

- [**Frappe Framework**](https://github.com/frappe/frappe): A full-stack web application framework written in Python and JavaScript. The framework provides a robust foundation for building web applications, including a database abstraction layer, user authentication, and a REST API.

- [**Frappe UI**](https://github.com/frappe/frappe-ui): A Vue-based UI library, to provide a modern user interface. The Frappe UI library provides a variety of components that can be used to build single-page applications on top of the Frappe Framework.

## Production Setup

### Managed Hosting

You can try [Frappe Cloud](https://frappecloud.com), a simple, user-friendly, and sophisticated [open-source](https://github.com/frappe/press) platform to host Frappe applications reliably and securely.

It handles installation, setup, upgrades, monitoring, maintenance, and support of your Frappe deployments. It is a fully featured developer platform with an ability to manage and control multiple Frappe deployments.

<div>
	<a href="https://erpnext-demo.frappe.cloud/app/home" target="_blank" rel="noopener noreferrer">
		<picture>
			<source media="(prefers-color-scheme: dark)" srcset="https://frappe.io/files/try-on-fc-white.png">
			<img src="https://frappe.io/files/try-on-fc-black.png" alt="Try on Frappe Cloud" height="28" />
		</picture>
	</a>
</div>


### Self-Hosted
#### Docker

See [Frappe Docker Documentation](https://github.com/frappe/frappe_docker) for full documentation & FAQ on Docker setup

#### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose v2](https://docs.docker.com/compose/)
- [git](https://docs.github.com/en/get-started/getting-started-with-git/set-up-git)

> For Docker basics and best practices refer to Docker's [documentation](https://docs.docker.com)

#### Demo setup

The fastest way to try ERPNext is to play in a pre-configured sandbox, in your browser, click the button below:

<a href="https://labs.play-with-docker.com/?stack=https://raw.githubusercontent.com/frappe/frappe_docker/main/pwd.yml">
  <img src="https://raw.githubusercontent.com/play-with-docker/stacks/master/assets/images/button.png" alt="Try in PWD"/>
</a>

### Try on your environment

> **⚠️ Disposable demo only**
>
> **This setup is intended for quick evaluation. Expect to throw the environment away.** You will not be able to install custom apps to this setup. For production deployments, custom configurations, and detailed explanations, see the full documentation.

First clone the repo:

```sh
git clone https://github.com/frappe/frappe_docker
cd frappe_docker
```

Then run:

```sh
docker compose -f pwd.yml up -d
```
Wait for a couple of minutes for ERPNext site to be created or check the `create-site` container logs before opening browser on port `8080`. (username: `Administrator`, password: `admin`)

See [Frappe Docker](https://github.com/frappe/frappe_docker/blob/main/docs/01-getting-started/03-arm64.md) for ARM based docker setup


## Development Setup
### Manual Install

The Easy Way: our install script for bench will install all dependencies (e.g. MariaDB). See https://github.com/frappe/bench for more details.

New passwords will be created for the ERPNext "Administrator" user, the MariaDB root user, and the Frappe user (the script displays the passwords and saves them to ~/frappe_passwords.txt).


## Learning and community

1. [Frappe School](https://school.frappe.io) - Learn Frappe Framework and ERPNext from the various courses by the maintainers or from the community.
2. [Official documentation](https://docs.erpnext.com/) - Extensive documentation for ERPNext.
3. [Discussion Forum](https://discuss.erpnext.com/) - Engage with community of ERPNext users and service providers.
4. [Telegram Group](https://erpnext_public.t.me) - Get instant help from huge community of users.


## Contributing

1. [Issue Guidelines](https://github.com/frappe/erpnext/wiki/Issue-Guidelines)
2. [Report Security Vulnerabilities](https://erpnext.com/security)
3. [Pull Request Requirements](https://github.com/frappe/erpnext/wiki/Contribution-Guidelines)
4. [Translations](https://crowdin.com/project/frappe)


## License

GNU/General Public License (see [license.txt](license.txt))

The ERPNext code is licensed as GNU General Public License (v3) and the Documentation is licensed as Creative Commons (CC-BY-SA-3.0) and the copyright is owned by Frappe Technologies Pvt Ltd (Frappe) and Contributors.

By contributing to ERPNext, you agree that your contributions will be licensed under its GNU General Public License (v3).

## Logo and Trademark Policy

Please read our [Logo and Trademark Policy](TRADEMARK_POLICY.md).
