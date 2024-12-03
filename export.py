from library import *
import plot
from openpyxl.styles import Alignment

def run(Data_Lib):
    # Create a new workbook and add a worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Figures"

    # Set up headers
    ws.append(['Date', 'Time', 'Description', 'UAV ID', 'Remark', "Image"])

    # In-memory list to store images for Excel
    img_buffers = []

    for files in Data_Lib:
        try:
            for Option in ["UAV vs Pri Baro", "UAV vs Sec Baro", "Pri Baro vs Sec Baro"]:
                # Generate the plot for each file and option and return the figure
                fig, status = plot.run(Data_Lib[files], Option, toggle=0)

                # Create an in-memory buffer for the image based on status
                img_buffer = io.BytesIO()
                if status == 10: 
                    fig.write_image(img_buffer, format='jpg')
                    img_name = f"{files}_{Option}_{str(Data_Lib[files]['UAV ID'].iloc[0])}_Below Cross-Check Offset.jpg"
                elif status == 11:
                    fig.write_image(img_buffer, format='jpg')
                    img_name = f"{files}_{Option}_{str(Data_Lib[files]['UAV ID'].iloc[0])}_Above Cross-Check Offset.jpg"
                elif status == 111:
                    fig.write_image(img_buffer, format='jpg')
                    img_name = f"{files}_{Option}_{str(Data_Lib[files]['UAV ID'].iloc[0])}_Cross-Check Fail.jpg"
                else:
                    fig.write_image(img_buffer, format='jpg')
                    img_name = f"{files}_{Option}_{str(Data_Lib[files]['UAV ID'].iloc[0])}_Below Offset.jpg"
                
                # Add the image buffer to the list (for embedding in Excel later)
                img_buffers.append((img_name, img_buffer))

        except Exception as e:
            st.write(f"Error processing file {files} with option {Option}: {e}")
            continue

    # Create Excel in-memory
    img_column_width = 100
    for row_index, (img_name, img_buffer) in enumerate(img_buffers, start=2):
        try:
            # Extract the file name and split
            filename_without_extension = os.path.splitext(os.path.basename(img_name))[0]
            filename_parts = filename_without_extension.split('_')

            # Add filename parts into separate columns
            for col_index, part in enumerate(filename_parts, start=1):
                cell = ws.cell(row=row_index, column=col_index, value=part)
                cell.alignment = Alignment(horizontal='left', vertical='top')  # Top-left alignment

            # Insert the image into the Excel sheet from the in-memory buffer
            img_buffer.seek(0)  # Ensure buffer is at the start
            excel_img = Image(img_buffer)
            cell_address = f"F{row_index}"
            ws.add_image(excel_img, cell_address)

            # Set row height to accommodate the image
            ws.row_dimensions[row_index].height = excel_img.height

        except Exception as e:
            st.write(f"Error inserting image {img_name} into Excel: {e}")
            continue

    # Set column dimensions for better formatting
    ws.column_dimensions["A"].width = 15  # Date
    ws.column_dimensions["B"].width = 15  # Time
    ws.column_dimensions["C"].width = 20  # Description
    ws.column_dimensions["D"].width = 15  # UAV ID
    ws.column_dimensions["E"].width = 30  # Remark
    ws.column_dimensions["F"].width = img_column_width  # Image column

    # Save the workbook to an in-memory buffer
    excel_buffer = io.BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)  # Rewind buffer to the beginning

    # Return the in-memory Excel buffer for download
    return excel_buffer

