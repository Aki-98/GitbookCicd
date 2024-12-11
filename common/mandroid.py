from apkutils import APK


def get_package_name(apk_path):
    # Initialize the APK object from the file
    with APK.from_file(apk_path) as apk:
        # Parse the resources, including the manifest
        apk.parse_resource()
        # Extract package name
        package_name = apk.get_package_name()
    return package_name


def get_version_name(apk_path):
    # Initialize the APK object from the file
    with APK.from_file(apk_path) as apk:
        # Parse the resources, including the manifest
        apk.parse_resource()
        # Extract version name and version code
        version_name = apk._version_name
    return version_name


def get_version_code(apk_path):
    # Initialize the APK object from the file
    with APK.from_file(apk_path) as apk:
        # Parse the resources, including the manifest
        apk.parse_resource()
        # Extract version name and version code
        version_code = apk._version_code
    return version_code


def get_apk_info(apk_path):
    # Initialize the APK object from the file
    with APK.from_file(apk_path) as apk:
        # Parse the resources, including the manifest
        apk.parse_resource()
        # Extract package name
        package_name = apk.get_package_name()
        # Extract version name and version code
        version_name = apk._version_name
        version_code = apk._version_code
    return package_name, version_name, version_code
