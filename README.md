# add-contributors

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b8d0af034c5c4699805c6aca898787e7)](https://app.codacy.com/manual/bobankhshen/add-contributors?utm_source=github.com&utm_medium=referral&utm_content=BobAnkh/add-contributors&utm_campaign=Badge_Grade_Dashboard)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/BobAnkh/add-contributors?color=orange&logo=github-actions)
![language-python](https://img.shields.io/github/languages/top/BobAnkh/add-contributors?logo=python&logoColor=yellow)
![LICENSE Apache-2.0](https://img.shields.io/github/license/BobAnkh/add-contributors?logo=apache)

A Github Action to add contributors to your markdown file(i.e. README.md) automatically on schedule or triggered by events

Specifically handle unreachable Chinese context (着重解决了中文内容乱码的问题)

Feel free to submit a pull request or an issue, but make sure to follow the templates

Welcome contributors to improve this project together!

## Usage

Create a workflow file such as `.github/workflows/contributors.yml` (you can find it in this repo)

```yaml
name: Add contributors
on:
  schedule:
    - cron:  '20 20 * * *'
# push:
#   branches:
#     - master

jobs:
  add-contributors:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: BobAnkh/add-contributors@master
      with:
        CONTRIBUTOR: '### Dev stack'
        COLUMN_PER_ROW: '6'
        ACCESS_TOKEN: ${{secrets.GITHUB_TOKEN}}
        IMG_WIDTH: '100'
        FONT_SIZE: '14'
        PATH: '/README.md'
        COMMIT_MESSAGE: 'docs(README): update contributors'
        AVATAR_SHAPE: 'round'
```

### Parameters

| Parameter            | Description                                                 | Required | Default                                            |
| -------------------- | ----------------------------------------------------------- | -------- | -------------------------------------------------- |
| REPO_NAME            | Repository name                                             | no       | `''` which means current repository                |
| CONTRIBUTOR          | Where you want to add contributors list                     | no       | `### Dev stack`                                 |
| COLUMN_PER_ROW       | Number of contributors per row                              | no       | `6`                                                |
| ACCESS_TOKEN         | Github Access Token                                         | yes      | You can just pass `${{secrets.GITHUB_TOKEN}}`      |
| IMG_WIDTH            | Width of img                                                | no       | `100`                                              |
| FONT_SIZE            | Font size of name (px)                                      | no       | `14`                                               |
| PATH                 | Path to the file you want to add contributors' list         | no       | `/README.md`                                       |
| BRANCH               | The branch to update file specified in PATH                 | no       | `''` which means default branch                    |
| PULL_REQUEST         | Open a new pull request if set to a target branch name      | no       | `''` which means not open pull request by default  |
| COMMIT_MESSAGE       | commit message                                              | no       | `docs(README): update contributors`                |
| AVATAR_SHAPE         | Set `round` for round avatar and `square` for square avatar | no       | square                                             |
| IGNORED_CONTRIBUTORS | Ignored contributors, seperated by comma                    | no       | `''`                                               |

> NOTE: You should leave a blank line after the `CONTRIBUTOR` line for the first time
>
> NOTE: Github seems not support image style in markdown file rendering yet
>
> NOTE: `IGNORED_CONTRIBUTORS` takes **display name** not **username**
> 
> NOTE: `PULL_REQUEST` must be used with `BRANCH` together, both **should be provided** if you want to **open a pull request**

## Maintainer

[@BobAnkh](https://github.com/BobAnkh)

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
    <th>Type</th>
    <th>Package</th>
    <th>Version</th>

</tr>
<tr>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        Package manager
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="pnpm" href="https://pnpm.io">
            <img style="width:fit-content; height:50px;" src="https://user-images.githubusercontent.com/4253088/196271039-0b998d0d-5867-47bf-a627-e36825175aeb.png"  alt="pnpm"/>
        </a>
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/pnpm">
            <img src="https://img.shields.io/badge/6.14.2-yellow"  alt="pnpm"/>
        </a>
    </td>

    
</tr>
<tr>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        Monorepo manager
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="turbo" href="https://turborepo.org/docs">
            <img style="width:fit-content; height:50px;" src="https://user-images.githubusercontent.com/4253088/196269627-8da367d0-5e1a-40a6-b261-d0f4e00498c1.png"  alt="turbo"/>
        </a>
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/turbo">
            <img src="https://img.shields.io/badge/1.6.3-brightgreen"  alt="turbo"/>
        </a>
    </td>

    
</tr>
<tr>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        CSS Framework
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="tailwindcss" href="https://tailwindcss.com/docs/installation">
            <img style="width:fit-content; height:50px;" src="https://user-images.githubusercontent.com/4253088/196271439-de4d436c-fb47-4a7e-84a6-fcc01d86026b.png"  alt="tailwindcss"/>
        </a>
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/tailwindcss">
            <img src="https://img.shields.io/badge/3.2.1-brightgreen"  alt="tailwindcss"/>
        </a>
    </td>

    
</tr>
<tr>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        Test runner
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="vitest" href="https://vitest.dev/">
            <img style="width:fit-content; height:50px;" src="https://user-images.githubusercontent.com/4253088/196270525-cea1d088-d329-4dba-879d-5e48ef779544.png"  alt="vitest"/>
        </a>
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/vitest">
            <img src="https://img.shields.io/badge/0.25.3-brightgreen"  alt="vitest"/>
        </a>
    </td>

    
</tr>
<tr>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        Testing components
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="@testing-library/react" href="https://testing-library.com/docs/react-testing-library/intro/">
            <img style="width:fit-content; height:50px;" src="https://user-images.githubusercontent.com/4253088/196271647-0265eca3-61e4-44c2-8641-fabdb07e875f.png"  alt="@testing-library/react"/>
        </a>
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/@testing-library/react">
            <img src="https://img.shields.io/badge/13.4.0-brightgreen"  alt="@testing-library/react"/>
        </a>
    </td>

    
</tr>
<tr>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        Component library
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="storybook" href="https://storybook.js.org/docs/react/get-started/introduction">
            <img style="width:fit-content; height:50px;" src="https://user-images.githubusercontent.com/321738/63501763-88dbf600-c4cc-11e9-96cd-94adadc2fd72.png"  alt="storybook"/>
        </a>
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/storybook">
            <img src="https://img.shields.io/badge/5-yellow"  alt="storybook"/>
        </a>
    </td>

    
</tr>
<tr>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        Lint
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="eslint" href="https://eslint.org/docs/user-guide/getting-started">
            Eslint
        </a>
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/eslint">
            <img src="https://img.shields.io/badge/7.32.0-yellow"  alt="eslint"/>
        </a>
    </td>

    
</tr>
<tr>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        Lint
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="husky" >
            Husky
        </a>
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/husky">
            <img src="https://img.shields.io/badge/8.0.1-brightgreen"  alt="husky"/>
        </a>
    </td>

    
</tr>
<tr>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        Lint
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="lint-staged" >
            Lint-staged
        </a>
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/lint-staged">
            <img src="https://img.shields.io/badge/12.0.3-brightgreen"  alt="lint-staged"/>
        </a>
    </td>

    
</tr>
<tr>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        Lint
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="prettier" >
            Prettier
        </a>
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a aria-label="NPM Version" href="https://www.npmjs.com/package/prettier">
            <img src="https://img.shields.io/badge/2.7.1-brightgreen"  alt="prettier"/>
        </a>
    </td>

    
</tr>
</table>

## LICENSE

[Apache-2.0](/LICENSE) © BobAnkh
