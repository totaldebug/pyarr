************
Contributing
************

Modifying the module
====================

It is recommended that contributions to this project are created within vscode,
utilising the devcontainer functionality.

This ensures that all developers are using the same environment and reduces the
risk of adding bugs / issues within the project.

.. note::
    The setup of VSCode devcontainer is outside of the scope of this document
    additional information can be found within the VSCode documentation.

Making changes
--------------

#. Fork the repository
#. Must follow PEP8 and Black formatting.
#. pyproject.toml must be updated with a new version, the new versions should
   follow `semver <http://semver.org/>`.
#. Re-generate API rst with sphinx
   ..code:: Python
      sphinx-apidoc -o ./docs ./pyarr
#. Each change should have its own PR.
#. All information should be filled out in the PR Template.
#. Any PR that consists of multiple changes may be rejected.
#. PRs must state if they are breaking changes and what would break by implementing.


Releasing the module
====================

To release a new version of the module, core team will take the following steps:

#. Reviewing and testing the PR that has been submitted to ensure all
   requirements have been met.
#. Tag the release in git: ``git tag $NEW_VERSION``.
#. Push the tag to GitHub: ``git push --tags origin``.
#. If all tests complete the package will be automatically released to PyPI
#. Github Action will re-create the documentation with Sphinx
