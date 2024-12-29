from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from helper import extract_numeric_value, resize_and_format_image, define_classe, round_usd_price, round_egp_price#,translate
#from deep_translator import GoogleTranslator as Translator
import math
import os


####################################################################################################################
####################################################################################################################


class PdfGenerator:
    def __init__(
            self, api_data, input_data, selected_language, use_manual_data, title, selected_images, image_manual, **kwargs
    ):
        # Global Variables
        self.api_data = api_data
        self.input_data = input_data
        quotation_num = self.input_data.get("quotation_num")
        self.selected_language = selected_language
        self.use_manual_data = use_manual_data
        self.img_root_path = f"/home/GoExport1/WebApp/images/{quotation_num}"
        self.title = title
        self.selected_images = selected_images
        self.image_manual = image_manual
        self.kwargs = kwargs


        # Define All Pages Size
        self.pdf_filename = self._generate_pdf_filename()
        self.page_width, self.page_height = 2481, 3508
        directory_path = f"/home/GoExport1/WebApp/PDFS/{quotation_num}/"
        pdf_path = f"{directory_path}/{self.pdf_filename}"
# Create the directory
        os.makedirs(directory_path, exist_ok=True)

        self.c = canvas.Canvas(
            pdf_path, pagesize=(self.page_width, self.page_height)
        )
        self._register_fonts()

        ####################################################################################################################
        ####################################################################################################################

    # Global Helper Functions



    def _generate_pdf_filename(self):
        model = self.api_data.get("model", "NA")
        manufacturer_brand = self.api_data.get("manufacturer_brand", "NA")
        purchaser_name = self.input_data.get("purchaser_name", "NA").replace(" ", "")
        index = self.input_data.get("Index", 0)
        date = datetime.today().strftime("%d.%m.%Y")
        return f"Export Offer-GO_00{index}-{purchaser_name}-{manufacturer_brand}-{model}-{date}.pdf"

    def _register_fonts(self):
        fonts = [
            ("AktivGrotesk-Regular", "AktivGrotesk-Regular.ttf"),
            ("AktivGrotesk-Medium", "AktivGrotesk-Medium.ttf"),
            ("AktivGrotesk-MediumItalic", "AktivGrotesk-MediumItalic.ttf"),
            ("AktivGrotesk-Bold", "AktivGrotesk-Bold.ttf"),
        ]
        for font_name, font_file in fonts:
            pdfmetrics.registerFont(TTFont(font_name, f"/home/GoExport1/WebApp/Assets/{font_file}"))

    def add_car_specs(self, specs, x1, y1, x2, y2, font_name="AktivGrotesk-Regular", font_size=22, bold_font_name="AktivGrotesk-Bold", bold_font_size=34):


            # Maximum number of elements per column
            max_elements_per_column = 16

            # Calculate the number of columns needed
            num_columns = math.ceil(len(specs) / max_elements_per_column)

            # Set initial font for measuring strings
            self.c.setFont(font_name, font_size)
            # Calculate line height based on font size
            line_height = font_size * 1.9  # Adjust line height as needed

            # Define headers to be bolded
            headers = ["Comfort & Convenience", "Entertainment & Media", "Safety & Security",
                    "Parking & Camera", "Performance", "Interior", "Exterior", "Packages", "Extras"]

            # Measure the width of the specs to determine padding
            column_widths = []
            for column_number in range(num_columns):
                # Get the subset of specs for the current column
                start_index = column_number * max_elements_per_column
                end_index = start_index + max_elements_per_column
                column_specs = specs[start_index:end_index]

                # Find the longest spec in this column
                max_width = 0
                for spec in column_specs:
                    if spec in headers:
                        self.c.setFont(bold_font_name, bold_font_size)  # Use bold font for headers
                        width = self.c.stringWidth(spec, bold_font_name, bold_font_size)
                    else:
                        self.c.setFont(font_name, font_size)  # Use regular font for other specs
                        width = self.c.stringWidth("• " + spec, font_name, font_size)
                    max_width = max(max_width, width)

                # Add some padding to the column width
                column_widths.append(max_width + 50)  # Add 50 units of padding

            # Draw the specs in columns
            for column_number in range(num_columns):
                x_position = x1 + sum(column_widths[:column_number])
                y_position = y1
                if column_number > 0:
                    y_position += 80  # Adjust starting Y position for subsequent columns
                    max_elements_per_column = 18

                # Get the subset of specs for the current column
                start_index = column_number * max_elements_per_column
                end_index = start_index + max_elements_per_column
                column_specs = specs[start_index:end_index]

                # Draw each spec in the column
                for spec in column_specs:
                    if spec in headers:
                        self.c.setFont(bold_font_name, bold_font_size)
                        self.c.drawString(x_position, y_position, spec)
                        adjusted_line_height = bold_font_size * 1.2
                    else:
                        self.c.setFont(font_name, font_size)
                        self.c.drawString(x_position, y_position, "• " + spec)
                        adjusted_line_height = line_height

                    y_position -= adjusted_line_height

        ####################################################################################################################
        ####################################################################################################################

    def generate_pdf(self):

        # Color Of PDF
        self.c.setFillColorRGB(0, 0, 0)

        ####################################################################################################################

        ###### Page 1 ######

        # Background Of The First Page
        self.c.drawImage(
            "/home/GoExport1/WebApp/Assets/Page_1.jpg", 0, 0, width=self.page_width, height=self.page_height
        )

        ####################################################################################################################

        # Seler & Client Info

        # Font
        self.c.setFont("AktivGrotesk-Medium", 32)

        # Quotation Data (Number)
        quotation_num = self.input_data.get("quotation_num", "")
        self.c.drawString(105, self.page_height - 175, "Quotation Number: ")

        self.c.drawString(405, self.page_height - 175, f"{quotation_num}")

        # Client Data (Name - Title)
        self.c.drawString(105, self.page_height - 230, "Client Name: ")
        purchaser_name = self.input_data.get("purchaser_name", "(PURCHASER NAME)")
        self.c.drawString(305, self.page_height - 230, f"{purchaser_name}")

        # Seller Data (Name - Phone)

        seller_name = self.input_data.get("seller_name", "Mr.")
        self.c.drawString(105, self.page_height - 285, "Prepared By: ")

        self.c.drawString(305, self.page_height - 285, f"{seller_name}")

        seller_phone = self.input_data.get("seller_phone", "xxxxxxxxxxx")
        self.c.drawString(105, self.page_height - 340, "Phone: ")

        self.c.drawString(250, self.page_height - 340, f"{seller_phone}")

        ####################################################################################################################

        # Car Title
        self.c.setFont("AktivGrotesk-Medium", 80)
        car_title = self.api_data.get("car_title", "NA")
        title = self.title
        if title:
            print_title = title
        else:
            print_title = car_title
        text_width = self.c.stringWidth(print_title, "AktivGrotesk-Medium", 80)
        x_position = (self.page_width - text_width) / 2
        self.c.drawString(x_position, self.page_height - 620, f"{print_title}")


        ####################################################################################################################


        selected_images = self.selected_images
        if selected_images is not None:
            length = len(selected_images)


        if self.image_manual:
            image1_path = ('/home/GoExport1/WebApp/images/' + selected_images[0])
            image2_path = "/home/GoExport1/WebApp/images/" + selected_images[1]

        else:


            selected_images_from_folder = define_classe(f"/home/GoExport1/WebApp/images/{quotation_num}/car parts")


            image1_path = f"/home/GoExport1/WebApp/images/{quotation_num}/car parts/Full front view"
            image2_path = f"/home/GoExport1/WebApp/images/{quotation_num}/car parts/Back view"
            if not os.path.exists(image1_path) or not os.path.exists(image2_path):
                image1_path = f"/home/GoExport1/WebApp/images/{quotation_num}/car parts/{selected_images_from_folder['Side view']}"
                image2_path = f"/home/GoExport1/WebApp/images/{quotation_num}/car parts/{selected_images_from_folder['Side view']}"
            else:
                image1_path = f"/home/GoExport1/WebApp/images/{quotation_num}/car parts/{selected_images_from_folder['Full front view']}"
                image2_path = f"/home/GoExport1/WebApp/images/{quotation_num}/car parts/{selected_images_from_folder['Back view']}"




        # Left part - first image
        image1_x1, image1_y1 = 93, 689
        image1_x2, image1_y2 = 1237, 1589

        image1_path = resize_and_format_image(image1_path, 93, 689, 1237, 1589)

        self.c.drawImage(
            image1_path,
            image1_x1,
            self.page_height - image1_y2,
            width=image1_x2 - image1_x1,
            height=(image1_y2 - image1_y1) - 66,
        )

        # Right part - Second image
        image2_x1, image2_y1 = 1241, 689
        image2_x2, image2_y2 = 2385, 1589

        image2_path = resize_and_format_image(image2_path, 1241, 689, 2385, 1589)

        self.c.drawImage(
            image2_path,
            image2_x1,
            self.page_height - image2_y2,
            width=image2_x2 - image2_x1,
            height=(image2_y2 - image2_y1) - 66,
        )

        ####################################################################################################################

        # Car Info
        self.c.setFont("AktivGrotesk-Regular", 45)
        #translator = Translator()
        #manufacturer_brand, firstregistration, fuel, transmission, model, mileage, color, power, translated_car_specs, car_shape = translate(
            #self.api_data, self.selected_language, translator)
        manufacturer_brand = self.api_data.get("manufacturer_brand", "NA")
        firstregistration = self.api_data.get("firstregistration", "NA")
        fuel = self.api_data.get("fuel", "NA")
        transmission = self.api_data.get("transmission", "NA")
        model = self.api_data.get("model", "NA")
        mileage = self.api_data.get("mileage", "NA")
        color = self.api_data.get("color", "NA")
        power = self.api_data.get("power", "NA")

        ## Left Info
        self.c.drawString(640, self.page_height - 1735, manufacturer_brand)
        self.c.drawString(640, self.page_height - 1790, firstregistration)
        self.c.drawString(640, self.page_height - 1855, fuel)
        self.c.drawString(640, self.page_height - 1915, transmission)

        ## Right Info
        self.c.drawString(1785, self.page_height - 1735, model)
        self.c.drawString(1785, self.page_height - 1790, mileage)
        self.c.drawString(1785, self.page_height - 1855, color)
        self.c.drawString(1785, self.page_height - 1915, power)


        ####################################################################################################################

        self.add_car_specs(
            self.api_data["car_features"],
            125,
            self.page_height - 2120,
            2240,
            self.page_height - 2760,
        )

        ####################################################################################################################

        # Financial Offer

        # Car Type or Customs Option
        Customs_option = self.input_data.get("Customs_option", 0)

        # Car Net Price
        gross = self.api_data.get("car_price", 0)
        car_net_price = float(gross) / 1.19

        # Euro Rate
        euroRate = self.input_data.get("euroRate")

        # Engine Size
        Engin_CC = self.api_data.get("EngineSize")
        if Engin_CC is None and fuel == "Electrical":
            Engin_CC = "Electrical"
        elif Engin_CC is None and fuel != "Electrical":
            Engin_CC = 0
        print("\nEngin_CC : ", Engin_CC)

        if Engin_CC != "Electrical":
            if Engin_CC == 0:
                stripped = 0
            else:
                stripped = extract_numeric_value(Engin_CC)
                print("\nstripped", stripped)
            if int(stripped) <= 1600:
                Engin_CC = str("upto 1600cc")
            elif 1600 < int(stripped) <= 2000:
                Engin_CC = str("1600-2000cc")
            elif int(stripped) > 2000:
                Engin_CC = str("more than 2000cc")

        # Country Of Origin

        # Germany Shipping & Egyptian Customs Calculations
        Germany_Shipping = self.input_data.get("Germany_Shipping", 0)
        Egyptian_Customs = self.input_data.get("Egyptian_Customs", 0)



        Egyptian_Customs = round(Egyptian_Customs)

        # Custom clearance fees (€)
        Port_Customs_Fees = self.input_data.get("Port_Customs_Fees", 0)

        print("***************")
        print(
            "car_net_price,Germany_Shipping,Port_Customs_Fees,Egyptian_Customs,euroRate"
        )
        print(
            car_net_price,
            Germany_Shipping,
            Port_Customs_Fees,
            Egyptian_Customs,
            euroRate,
        )
        print("***************")

        # Go Fees ($) & Customs Calculation

        Fees = self.input_data.get("G&O_Fees", 0)


        if Customs_option == "Used Car":
            # 1
            GOFees = (
                             ((car_net_price + Germany_Shipping + Port_Customs_Fees) * euroRate)
                             + Egyptian_Customs
                     ) * (Fees / 100)

            # 2
            customs = round(Port_Customs_Fees * euroRate) + Egyptian_Customs

        else:
            # 1
            GOFees = (
                             (
                                     (car_net_price + Germany_Shipping + Port_Customs_Fees)
                                     + (car_net_price * (Egyptian_Customs / 100))
                             )
                             * (Fees / 100)
                     ) * euroRate

            # 2
            customs = round(
                ((car_net_price * (Egyptian_Customs / 100)) + Port_Customs_Fees)
                * euroRate
            )

        print(f"GOFees {GOFees}")

        # Car Cost In Alexandria For Both New & Used
        Car_Cost_till_reaching_Alexandria = round_usd_price(round(((car_net_price + Germany_Shipping) * euroRate) + GOFees))

        customs = round_usd_price(customs)

        # Total Contract
        if self.input_data.get("egyptian_pound"):
            Total_Contract_Amount = round_egp_price(round((Car_Cost_till_reaching_Alexandria + customs) * self.input_data.get("dollar_rate")))

            Car_Cost_till_reaching_Alexandria = round_egp_price(round(Car_Cost_till_reaching_Alexandria * self.input_data.get("dollar_rate")))

            customs = round_egp_price(round(customs * self.input_data.get("dollar_rate")))
        else:
            Total_Contract_Amount = round_usd_price(round(Car_Cost_till_reaching_Alexandria + customs))

        # Formatted Numbers
        Car_Cost_till_reaching_Alexandria = "{:,}".format(
            Car_Cost_till_reaching_Alexandria
        )


        customs = "{:,}".format(customs)

        Total_Contract_Amount = "{:,}".format(Total_Contract_Amount)

        ## Get Destination City
        self.c.setFont("AktivGrotesk-Regular", 40)

        destination_city = self.input_data.get("destination_city", "Alexandria")
        self.c.drawString(150, self.page_height - 3065, f"Total Car cost till {destination_city} port")
        self.c.drawString(150, self.page_height - 3150, "Estimated Customs")

        ## Total Car Cost Till Alexandria Port & Estimated Customs
        if self.input_data.get("egyptian_pound"):
            self.c.setFont("AktivGrotesk-Regular", 45)
            self.c.drawString(150, self.page_height - 3065, f"{Car_Cost_till_reaching_Alexandria} EGP")
            self.c.drawString(895, self.page_height - 3150, f"{customs} EGP")

            ## Total Contract
            self.c.setFont("AktivGrotesk-Medium", 90)
            self.c.drawString(1750, self.page_height - 3090, f"{Total_Contract_Amount} EGP")

        else:
            self.c.setFont("AktivGrotesk-Regular", 45)
            self.c.drawString(895, self.page_height - 3065, f"{Car_Cost_till_reaching_Alexandria} USD")

            self.c.drawString(895, self.page_height - 3150, f"{customs} USD")

            ## Total Contract
            self.c.setFont("AktivGrotesk-Medium", 90)
            self.c.drawString(1750, self.page_height - 3090, f"{Total_Contract_Amount} USD")

        self.c.showPage()

        ####################################################################################################################
        ####################################################################################################################

        ###### Page 2 ######
        # Background Of The Second Page
        self.c.drawImage(
            "/home/GoExport1/WebApp/Assets/Page_2.jpg", 0, 0, width=self.page_width, height=self.page_height
        )


        if not self.image_manual:

            # Image 1
            image_path1 = f"/home/GoExport1/WebApp/images/{quotation_num}/car parts/{selected_images_from_folder['Interior'][0]}"

            image_path1 = resize_and_format_image(image_path1, 270, 448, 1229, 1200)

            self.c.drawImage(
                image_path1,
                270,
                self.page_height - 1200,
                width=1229 - 270,
                height=1200 - 448,
            )

            # Image 2
            image_path2 = f"/home/GoExport1/WebApp/images/{quotation_num}/car parts/{selected_images_from_folder['Interior'][1]}"

            image_path2 = resize_and_format_image(image_path2, 1251, 448, 2210, 1200)

            self.c.drawImage(
                image_path2,
                1251,
                self.page_height - 1200,
                width=2210 - 1251,
                height=1200 - 448,
            )

            # Image 3
            image_path3 = f"/home/GoExport1/WebApp/images/{quotation_num}/car parts/{selected_images_from_folder['Interior'][2]}"

            image_path3 = resize_and_format_image(image_path3, 500, 1506, 1979, 2300)

            self.c.drawImage(
                image_path3,
                500,
                self.page_height - 2100,
                width=1979 - 500,
                height=2300 - 1506,
            )

        # Draw the images on the second page at the specified positions
        if self.image_manual and length == 5:
            # Image 1

            image_path1 = "/home/GoExport1/WebApp/images/" + selected_images[2]

            image_path1 = resize_and_format_image(image_path1, 270, 448, 1229, 1200)

            self.c.drawImage(
                image_path1,
                270,
                self.page_height - 1200,
                width=1229 - 270,
                height=1200 - 448,
            )

            # Image 2
            image_path2 = "/home/GoExport1/WebApp/images/" + selected_images[3]

            image_path2 = resize_and_format_image(image_path2, 1251, 448, 2210, 1200)

            self.c.drawImage(
                image_path2,
                1251,
                self.page_height - 1200,
                width=2210 - 1251,
                height=1200 - 448,
            )

            # Image 3

            image_path3 = "/home/GoExport1/WebApp/images/" + selected_images[4]

            image_path3 = resize_and_format_image(image_path3, 500, 1506, 1979, 2300)

            self.c.drawImage(
                image_path3,
                500,
                self.page_height - 2100,
                width=1979 - 500,
                height=2300 - 1506,
            )

        elif self.image_manual and length == 4:
            # Image 1

            image_path1 = "/home/GoExport1/WebApp/images/" + selected_images[2]

            image_path1 = resize_and_format_image(image_path1, 80, 448, 1229, 1200)

            self.c.drawImage(
                image_path1,
                80,
                self.page_height - 1500,
                width=1229 - 80,
                height=1200 - 448,
            )

            # Image 2
            image_path2 = "/home/GoExport1/WebApp/images/" + selected_images[3]

            image_path2 = resize_and_format_image(image_path2, 1251, 448, 2400, 1200)

            self.c.drawImage(
                image_path2,
                1251,
                self.page_height - 1500,
                width=2400 - 1251,
                height=1200 - 448,
            )


        elif self.image_manual and length == 3:
            # Image 1

            image_path1 = "/home/GoExport1/WebApp/images/" + selected_images[2]

            image_path1 = resize_and_format_image(image_path1, 200, 50, 2270, 1248)

            self.c.drawImage(
                image_path1,
                200,
                self.page_height - 1850,
                width=2270 - 200,
                height=1248 - 50,
            )



        self.c.showPage()
        ####################################################################################################################
        ####################################################################################################################

        ###### Page 3 ######
        # Background Of The Third Page
        self.c.drawImage(
            "/home/GoExport1/WebApp/Assets/Page_3.jpg", 0, 0, width=self.page_width, height=self.page_height
        )

        self.c.showPage()

        ####################################################################################################################
        ####################################################################################################################


        self.c.save()
