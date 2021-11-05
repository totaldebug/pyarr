############
Contributing
############

It is recommended that contributions to this project are created within vscode,
utilising the devcontainer functionality.

This ensures that all developers are using the same environment and extentions.
This reduces the risk of additional bugs / formatting issues within the project.

.. note::
    The setup of VSCode devcontainer is outside of the scope of this document
    additional information can be found within the VSCode documentation.

**********************
Setup your environment
**********************

#. Fork the `repository <https://github.com/totaldebug/pyarr>`_
#. Open the repository in VSCode
#. Copy the .devcontainer/recommended-*** files and remove the "recommended-" text
#. Press ``ctrl + shift + p`` and select ``Remote-Container: Reopen in Container``
#. Once loaded you can begin modification of the module or Documentation

*********************
Updating PyArr module
*********************

Style & formatting
==================

It is highly recommended to use vsCode devcontainer as this automatically adds the
required formatting checks on pre-commit, this will allow for resolution of issues
prior to the pull request being submitted.

If you are not using devcontainer please register the pre-commit-config:

.. code:: bash
   poetry run pre-commit install

A few guidelines for approval:

- Must follow PEP8 / Black formatting. (devcontainer is setup to reformat on save)
- We recommend using `sourcery <https://sourcery.ai/>`_ to ensure code is most
  efficient, this will be checked when the pull reuqest is opened.
- All functions must use google docstring format, the devcontainer has an
   `autodocstring <https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring>`_
   plugin which will auto fill.
- ``pyproject.toml`` must be updated with a new version, the new versions should
   follow `semver <http://semver.org/>`_.
- Each feature / bugfix etc. should have its own pull request.

**********************
Updating Documentation
**********************

The documentation for this project utilises `sphinx <https://www.sphinx-doc.org/>`_.
Sphinx allows for automatic documenting of all classes / functions via DocString.

To Update static pages, you can amend the ``.rst`` files in the ``sphinx-docs`` folder.

All Python Class / Function documentation is updated automatically by Github Actions and
does not require any manual changes to be made.

Sphinx documentation uses `reStructuredText <https://docutils.sourceforge.io/rst.html>`_ to format each of the pages.

***********************
Pull Requests & Release
***********************

Now that you have made the changes required for your enhancement, a pull request
is required for the core team to review the changes, request amendements or approve
the work that you have completed.

Pull Requests
=============

- Each feature / bugfix should have its own PR. This makes code review more efficient
   and allows for a clean changelog generation
- If a Pull Request contains multiple changes, our core team may reject it
- All information in the Pull Request template should be completed, when people look
   at what was done with this Pull Request it should be easy to tell from this template
- It must state if the change is a Breaking Change, and what would break by implementing

Release Changes
=================

To release a new version of the module or documentation updates, the core team
 will take the following steps:

#. Reviewing and testing the PR that has been submitted to ensure all
   requirements have been met.
#. Tag the release in git: ``git tag $NEW_VERSION``.
#. Push the tag to GitHub: ``git push --tags origin``.
#. If all tests complete the package will be automatically released to PyPI
#. Github Action will re-create the documentation with Sphinx

If the only change is to documentation, the workflow ``Sphinx Documentation Update``
will be run to update the documentation.

Documentation updates don't require the version to be updated in ``pyproject.toml``
and also don't require tagging.
