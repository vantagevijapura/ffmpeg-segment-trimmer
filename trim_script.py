import subprocess
import os
import sys

def format_timestamp(ts):
    """Ensures input like 18:00 is converted to 00:18:00."""
    parts = ts.strip().split(':')
    if len(parts) == 2:
        return f"00:{parts[0].zfill(2)}:{parts[1].zfill(2)}"
    elif len(parts) == 1:
        return f"00:00:{parts[0].zfill(2)}"
    return ts.strip()

def main():
    if len(sys.argv) < 2:
        print("\nUsage: python script.py /path/to/video.mp4")
        return

    full_path = sys.argv[1].strip().replace("'", "").replace('"', "")
    
    if not os.path.exists(full_path):
        print(f"\nError: File not found at {full_path}")
        return

    video_dir = os.path.abspath(os.path.dirname(full_path))
    video_filename = os.path.basename(full_path)
    base_name = os.path.splitext(video_filename)[0]
    
    os.chdir(video_dir)

    try:
        num_cuts = int(input(f"\nProcessing: {video_filename}\nHow many segments? "))
    except ValueError:
        print("Invalid number.")
        return

    temp_files = []

    for i in range(num_cuts):
        print(f"\n--- Part {i+1} ---")
        start = format_timestamp(input("  Start Timestamp (MM:SS): "))
        end = format_timestamp(input("  End Timestamp (MM:SS): "))
        
        part_name = f"temp_part_{i+1}.mp4"
        
        # Using -to ensures it stops at the specific time, not after a duration
        cmd = [
            'ffmpeg',
            '-i', video_filename, 
            '-ss', start, 
            '-to', end, 
            '-c', 'copy', 
            part_name
        ]
        
        print(f"  Executing: Cut from {start} until it reaches {end}")
        subprocess.run(cmd)
        temp_files.append(part_name)

    list_filename = "mylist.txt"
    with open(list_filename, 'w') as f:
        for temp in temp_files:
            f.write(f"file '{temp}'\n")

    final_output = f"{base_name}_trimmed.mp4"
    merge_cmd = [
        'ffmpeg', '-y', 
        '-f', 'concat', 
        '-safe', '0', 
        '-i', list_filename, 
        '-c', 'copy', 
        final_output
    ]

    print(f"\nMerging parts into {final_output}...")
    subprocess.run(merge_cmd)

    # Cleanup
    if os.path.exists(list_filename):
        os.remove(list_filename)
    for temp in temp_files:
        if os.path.exists(temp):
            os.remove(temp)

    print(f"\nDone! Saved in: {video_dir}")

if __name__ == "__main__":
    main()