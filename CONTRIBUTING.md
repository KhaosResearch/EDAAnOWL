# How to Contribute

Thank you for your interest in contributing to EDAAnOWL!

## Reporting Issues

If you find a bug, inconsistency, or have a feature request, please [open an Issue](https://github.com/KhaosResearch/EDAAnOWL/issues) in the repository.

## Submitting Changes (General Contributions)

For minor fixes or feature additions that don't constitute a new version:

1.  **Fork & Branch:** Fork the repository and create a descriptive branch from the `dev` branch.

    ```bash
    # Make sure your dev is up to date
    git checkout dev
    git pull origin dev

    # Create your new branch
    git checkout -b fix/correct-typo-in-profile
    ```

2.  **Make Changes:** Modify the necessary `.ttl` files _within the latest version's folder_ (e.g., `src/0.0.1/`).
3.  **Commit & Push:** Commit your changes and push them to your fork.
4.  **Open a Pull Request:** Submit a PR against the `dev` branch for review.

---

## How to Publish a New Version (Core Maintainer Process)

Publishing a new version is a semi-automated process. It requires preparing all files in the `dev` branch, merging them into `main`, and then creating a GitHub Release.

**Example: Publishing version `0.0.2` (from `0.0.1`)**

### Step 1: Prepare the New Version on the `dev` Branch

All new development happens on the `dev` branch (or feature branches merged into it).

1.  **Duplicate the Version Folder:**

    - Create a copy of the entire directory for the last version and name it with the new version.
    - `cp -r src/0.0.1/ src/0.0.2/`

2.  **Update the Main Ontology File:**

    - Open the new file: `src/0.0.2/EDAAnOWL.ttl`.
    - Find and update the `owl:versionIRI` and `owl:versionInfo`:
      ```turtle
      # ...
      [https://w3id.org/EDAAnOWL/](https://w3id.org/EDAAnOWL/) rdf:type owl:Ontology ;
                                    owl:versionIRI [https://w3id.org/EDAAnOWL/0.0.2](https://w3id.org/EDAAnOWL/0.0.2) ; # <-- UPDATE
                                    owl:versionInfo "0.0.2"; # <-- UPDATE
      # ...
      ```
    - Find and update **all `owl:imports`** of your modular vocabularies to point to the new version path:
      ```turtle
      # ...
                                    owl:imports ...
                                                [https://w3id.org/EDAAnOWL/0.0.2/vocabularies/agro-vocab](https://w3id.org/EDAAnOWL/0.0.2/vocabularies/agro-vocab) , # <-- UPDATE
                                                [https://w3id.org/EDAAnOWL/0.0.2/vocabularies/datatype-scheme](https://w3id.org/EDAAnOWL/0.0.2/vocabularies/datatype-scheme) , # <-- UPDATE
                                                # ... (and so on for all vocabs)
      # ...
      ```

3.  **Update the Modular Vocabularies:**

    - For **each** `.ttl` file inside `src/0.0.2/vocabularies/`:
    - Open the file (e.g., `agro-vocab.ttl`).
    - Update its `@base` and `owl:Ontology` URI to the new version:

      ```turtle
      # ...
      @base [https://w3id.org/EDAAnOWL/0.0.2/vocabularies/agro-vocab](https://w3id.org/EDAAnOWL/0.0.2/vocabularies/agro-vocab) . # <-- UPDATE

      [https://w3id.org/EDAAnOWL/0.0.2/vocabularies/agro-vocab](https://w3id.org/EDAAnOWL/0.0.2/vocabularies/agro-vocab) rdf:type owl:Ontology ; # <-- UPDATE
          owl:imports [https://w3id.org/EDAAnOWL/0.0.2/vocabularies/sector-scheme](https://w3id.org/EDAAnOWL/0.0.2/vocabularies/sector-scheme) ; # <-- UPDATE (if it imports others)
      # ...
      ```

4.  **Make All Other Changes:** Add, modify, or remove any concepts, properties, etc., within the `src/0.0.2/` files.
5.  **Update the Changelog:** Edit `CHANGELOG.md` to document all the new changes under an `[Unreleased]` section.
6.  **Commit:** Commit all your changes to the `dev` branch.
    - `git add .`
    - `git commit -m "feat: Prepare files and changes for v0.0.2"`
    - `git push origin dev`

### Step 2: Merge `dev` into `main`

1.  When the `dev` branch is stable and all files for the new version are ready, open a Pull Request from `dev` to `main`.
2.  Title the PR: "Merge `dev` into `main` for v0.0.2 Release".
3.  Have the PR reviewed and approved by a maintainer.
4.  **Merge the Pull Request.** The `main` branch now contains the new `src/0.0.2/` folder and is ready to be tagged.

### Step 3: Create the GitHub Release (Triggers Automation)

This is the final step that makes the new version public.

1.  Go to the **"Releases"** page of the repository.
2.  Click **"Draft a new release"**.
3.  Click "Choose a tag" and **create a new tag**. The tag **MUST** use the `vX.Y.Z` format (with a `v`).
    - Example: `v0.0.2`
4.  Ensure the "Target" is the **`main` branch** (which you just merged into).
5.  Set the release title (e.g., "Version 0.0.2").
6.  Copy the notes from `CHANGELOG.md` for the new version into the release description.
7.  Update the `CHANGELOG.md` file itself: change `[Unreleased]` to `[0.0.2] - YYYY-MM-DD` and add the comparison links at the bottom. Commit this change to `main`.
8.  Click **"Publish release"**.

### Step 4: Done!

Publishing the release triggers the `release.yml` workflow. It will:

- Detect the tag `v0.0.2`.
- Get the version string `0.0.2`.
- Use the files from `src/0.0.2/` to run Widoco.
- Run the **Step 7 (Post-process)** `sed` command to fix vocabulary links.
- Run the **Step 8 (Prepare files)** to:
  - Copy all files into `deploy/0.0.2/`.
  - Sync `deploy/latest/` to mirror the new version.
- Push the final `deploy/` directory to the `gh-pages` branch.

Wait ~5 minutes, then verify that `https://w3id.org/EDAAnOWL/latest/` and `https://w3id.org/EDAAnOWL/0.0.2/` are working correctly.
