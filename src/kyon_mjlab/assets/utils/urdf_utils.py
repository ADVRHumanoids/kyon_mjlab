import rospkg
from pathlib import Path
rospack = rospkg.RosPack()

def parse_xacro(xacro_path: Path, args: dict[str, str]) -> str:
    """
    Parse a xacro file and return the resulting URDF string.
    """
    import subprocess
    xacro_cmd = f'xacro {xacro_path} ' + ' '.join([f'{k}:={v}' for k, v in args.items()])
    print(f'[INFO] Generating URDF with command: {xacro_cmd}')
    urdf = subprocess.check_output(xacro_cmd, shell=True, text=True)
    print(f'[INFO] Generated URDF length: {len(urdf)}')
    return urdf

def add_mujoco_compiler_tag(urdf: str) -> str:
    """
    Add a <mujoco> tag with <compiler strippath="false"/> to the URDF string if not present.
    """
    if '<mujoco>' in urdf:
        return urdf  # Already has mujoco tag

    # Find the line with <robot ...>
    # add the additional <mujoco> tag as child of <robot>
    _ROBOT_LINE = None 
    for line in urdf.splitlines():
        if '<robot' in line:
            _ROBOT_LINE = line
            break
        
    if _ROBOT_LINE is None:
        raise ValueError("URDF does not contain a <robot> tag.")

    MUJOCO_TAG = f"""
    {_ROBOT_LINE}
    <mujoco>
        <compiler strippath="false"/>
    </mujoco>
    """

    return  urdf.replace(_ROBOT_LINE, MUJOCO_TAG)


def resolve_package_paths(urdf: str) -> str:
    """
    Resolve 'package://' paths in a URDF string to absolute file system paths.
    """
    import re
    pattern = r'package://([^/]+)/([^"\s]+)'
    def replace_match(match):
        package_name = match.group(1)
        relative_path = match.group(2)
        try:
            package_path = rospack.get_path(package_name)
            full_path = Path(package_path) / relative_path
            return str(full_path)
        except rospkg.ResourceNotFound:
            print(f"[WARNING] Package '{package_name}' not found. Leaving path unchanged.")
            return match.group(0)
    return re.sub(pattern, replace_match, urdf)