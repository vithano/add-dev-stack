# add-add-stack

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b8d0af034c5c4699805c6aca898787e7)](https://app.codacy.com/manual/vithano/add-dev-stack?utm_source=github.com&utm_medium=referral&utm_content=vithano/add-dev-stack&utm_campaign=Badge_Grade_Dashboard)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/vithano/add-dev-stack?color=orange&logo=github-actions)
![language-python](https://img.shields.io/github/languages/top/vithano/add-dev-stack?logo=python&logoColor=yellow)
![LICENSE Apache-2.0](https://img.shields.io/github/license/vithano/add-dev-stack?logo=apache)

A Github Action to add a dev stack to your markdown file(i.e. README.md) automatically on schedule or triggered by events

Specifically handle unreachable Chinese context (着重解决了中文内容乱码的问题)

Feel free to submit a pull request or an issue, but make sure to follow the templates

Welcome contributors to improve this project together!

## Usage

Create a workflow file such as `.github/workflows/dev-stack.yml` (you can find it in this repo)

```yaml
name: Add dev stack
on:
  schedule:
    - cron:  '20 20 * * *'
push:
  branches:
    - master
  paths:
    - "package.json"

jobs:
  add-dev-stack:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: vithano/add-dev-stack@master
      with:
        CONTRIBUTOR: '### Dev stack'
        ACCESS_TOKEN: ${{secrets.GITHUB_TOKEN}}
        IMG_WIDTH: '50'
        FONT_SIZE: '18'
        PATH: '/README.md'
        COMMIT_MESSAGE: 'docs(README): update dev stack'
        AVATAR_SHAPE: 'round'
        TYPES_TO_SHOW: 'Package manager,Monorepo manager,Frontend Framework,CSS Framework,Server-client communication,Backend Framework,ORM,Test runner,Testing components,Component library,Mocking,Lint'
```

### Parameters

| Parameter            | Description                                                 | Required | Default                                            |
| -------------------- | ----------------------------------------------------------- | -------- | -------------------------------------------------- |
| REPO_NAME            | Repository name                                             | no       | `''` which means current repository                |
| CONTRIBUTOR          | Where you want to add contributors list                     | no       | `### Dev stack`                                 |
| COLUMN_PER_ROW       | Number of contributors per row                              | no       | `6`                                                |
| ACCESS_TOKEN         | Github Access Token                                         | yes      | You can just pass `${{secrets.GITHUB_TOKEN}}`      |
| IMG_WIDTH            | Width of avatar                                                | no       | `100`                                              |
| FONT_SIZE            | Font size of name (px)                                      | no       | `14`                                               |
| PATH                 | Path to the file you want to add contributors' list         | no       | `/README.md`                                       |
| BRANCH               | The branch to update file specified in PATH                 | no       | `''` which means default branch                    |
| PULL_REQUEST         | Open a new pull request if set to a target branch name      | no       | `''` which means not open pull request by default  |
| COMMIT_MESSAGE       | commit message                                              | no       | `docs(README): update dev stack`                |
| AVATAR_SHAPE         | Set `round` for round avatar and `square` for square avatar | no       | square                                             |
| COLUMNS              | the column names                                            | no       | `'Type,Package,Version'`                |
| PACKAGES_TO_SHOW     | if you wish to show specific packages, you can specifiy their names                  | no       | `all`                |
| TYPES_TO_SHOW        | if you wish to show specific types or order them            | no       | `all`, Possible values are 'Package manager,Bundler,Test runner,UI Library,Frontend Framework,Frontend Language,GraphQL,Monorepo manager,CSS Framework,Server-client communication,Backend Framework,Mobile Framework,Testing components,ORM,Test runner,Component library,Documentation,Mocking,Lint                |
`''`                                               |

> NOTE: You should leave a blank line after the `### Dev stack` line for the first time
>
> NOTE: Github seems not support image style in markdown file rendering yet
> 
> NOTE: `PULL_REQUEST` must be used with `BRANCH` together, both **should be provided** if you want to **open a pull request**

## Maintainer

[@BobAnkh](https://github.com/vithano)

## How to contribute

You should follow our [Code of Conduct](/CODE_OF_CONDUCT.md).

See [CONTRIBUTING GUIDELINES](/CONTRIBUTING.md) for contributing conventions.

Make sure to pass all the tests before submitting your code. You can conduct `pytest -ra` at the root directory to run all tests.

You can use local mode when develope it on your local machine, here is the command-line help info:

```console
usage: main.py [-h] [-m MODE] [-f FILE] [-o OUTPUT] [-t TOKEN]

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  choose to use local-dev mode or on github action mode.
                        Valid values are 'local' or 'github'
  -f FILE, --file FILE  configuration file to read from when running local-dev
                        mode
  -o OUTPUT, --output OUTPUT
                        output file when running local-dev mode
  -t TOKEN, --token TOKEN
                        Github Access Token
```

### Dev stack

<table>
<tr>
    <th align="center" style="text-align:center;">Type</th>
    <th align="center" style="text-align:center;">Package</th>
    <th align="center" style="text-align:center;">Version</th>

</tr>
<tr style="padding-top:10px;">
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        Package manager
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a style="display: inline-flex;align-items: center;padding-top:10px;
    flex-direction: column; font-size:19px" aria-label="pnpm" href="https://pnpm.io">
            <img style="border-radius:6px;width:50px;height:50px; " src="https://avatars.githubusercontent.com/u/21320719?s=200&v=4" alt="pnpm"/>
                    </br>
                pnpm
        </a>
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/pnpm">
            <img src="https://img.shields.io/badge/6.14.2-red" alt="pnpm"/>
        </a>
    </td>

    
</tr>
<tr style="padding-top:10px;">
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        Monorepo manager
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a style="display: inline-flex;align-items: center;padding-top:10px;
    flex-direction: column; font-size:19px" aria-label="turbo" href="https://turborepo.org/docs">
            <img style="border-radius:6px;width:50px;height:50px; " src="https://user-images.githubusercontent.com/4060187/196936104-5797972c-ab10-4834-bd61-0d1e5f442c9c.png" alt="turbo"/>
                    </br>
                turbo
        </a>
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/turbo">
            <img src="https://img.shields.io/badge/1.10.14-brightgreen" alt="turbo"/>
        </a>
    </td>

    
</tr>
<tr style="padding-top:10px;">
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        CSS Framework
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a style="display: inline-flex;align-items: center;padding-top:10px;
    flex-direction: column; font-size:19px" aria-label="tailwindcss" href="https://tailwindcss.com/docs/installation">
            <img style="border-radius:6px;width:50px;height:50px; " src="https://avatars.githubusercontent.com/u/67109815?s=200&v=4" alt="tailwindcss"/>
                    </br>
                tailwindcss
        </a>
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/tailwindcss">
            <img src="https://img.shields.io/badge/3.2.1-brightgreen" alt="tailwindcss"/>
        </a>
    </td>

    
</tr>
<tr style="padding-top:10px;">
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        Test runner
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a style="display: inline-flex;align-items: center;padding-top:10px;
    flex-direction: column; font-size:19px" aria-label="vitest" href="https://vitest.dev/">
            <img style="border-radius:6px;width:50px;height:50px; " src="https://avatars.githubusercontent.com/u/95747107?s=200&v=4" alt="vitest"/>
                    </br>
                vitest
        </a>
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/vitest">
            <img src="https://img.shields.io/badge/0.34.6-brightgreen" alt="vitest"/>
        </a>
    </td>

    
</tr>
<tr style="padding-top:10px;">
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        Testing components
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a style="display: inline-flex;align-items: center;padding-top:10px;
    flex-direction: column; font-size:19px" aria-label="@testing-library/react" href="https://testing-library.com/docs/react-testing-library/intro/">
            <img style="border-radius:6px;width:50px;height:50px; " src="https://avatars.githubusercontent.com/u/49996085?s=200&v=4" alt="@testing-library/react"/>
                    </br>
                @testing-library/react
        </a>
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/@testing-library/react">
            <img src="https://img.shields.io/badge/13.4.0-yellow" alt="@testing-library/react"/>
        </a>
    </td>

    
</tr>
<tr style="padding-top:10px;">
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        Component library
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a style="display: inline-flex;align-items: center;padding-top:10px;
    flex-direction: column; font-size:19px" aria-label="storybook" href="https://storybook.js.org/docs/react/get-started/introduction">
            <img style="border-radius:6px;width:50px;height:50px; " src="https://avatars.githubusercontent.com/u/22632046?s=200&v=4" alt="storybook"/>
                    </br>
                storybook
        </a>
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/storybook">
            <img src="https://img.shields.io/badge/4-red" alt="storybook"/>
        </a>
    </td>

    
</tr>
<tr style="padding-top:10px;">
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        Lint
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a style="display: inline-flex;align-items: center;padding-top:10px;
    flex-direction: column; font-size:19px" aria-label="eslint" href="https://eslint.org/docs/user-guide/getting-started">
            <img style="border-radius:6px;width:50px;height:50px; " src="https://avatars.githubusercontent.com/u/6019716?s=200&v=4" alt="eslint"/>
                    </br>
                eslint
        </a>
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/eslint">
            <img src="https://img.shields.io/badge/7.32.0-yellow" alt="eslint"/>
        </a>
    </td>

    
</tr>
<tr style="padding-top:10px;">
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        Lint
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a style="display: inline-flex;align-items: center;padding-top:10px;
    flex-direction: column; font-size:19px" aria-label="husky" href="https://typicode.github.io/husky/">
            <img style="border-radius:6px;width:50px;height:50px; " src="https://res.cloudinary.com/practicaldev/image/fetch/s--3HkALzIp--/c_imagga_scale,f_auto,fl_progressive,h_420,q_auto,w_1000/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/v67mrvpgrqg19k3ifgll.png" alt="husky"/>
                    </br>
                husky
        </a>
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/husky">
            <img src="https://img.shields.io/badge/8.0.1-brightgreen" alt="husky"/>
        </a>
    </td>

    
</tr>
<tr style="padding-top:10px;">
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        Lint
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a style="display: inline-flex;align-items: center;padding-top:10px;
    flex-direction: column; font-size:19px" aria-label="lint-staged" href="https://github.com/okonet/lint-staged">
            Lint-staged
        </a>
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/lint-staged">
            <img src="https://img.shields.io/badge/12.0.3-red" alt="lint-staged"/>
        </a>
    </td>

    
</tr>
<tr style="padding-top:10px;">
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        Lint
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a style="display: inline-flex;align-items: center;padding-top:10px;
    flex-direction: column; font-size:19px" aria-label="prettier" href="https://prettier.io/docs/en/index.html">
            <img style="border-radius:6px;width:50px;height:50px; " src="https://avatars.githubusercontent.com/u/25822731?s=200&v=4" alt="prettier"/>
                    </br>
                prettier
        </a>
    </td>
    <td align="center" style="text-align:center;white-space: nowrap; width: 75.0px; height: 75.0px">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/prettier">
            <img src="https://img.shields.io/badge/2.7.1-yellow" alt="prettier"/>
        </a>
    </td>

    
</tr>
</table>

## LICENSE

[Apache-2.0](/LICENSE) © BobAnkh
