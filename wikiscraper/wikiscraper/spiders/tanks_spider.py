from pathlib import Path

import scrapy

# Run with scrapy wikiTank -o tankList.json
class WikiSpider(scrapy.Spider):
    name = "wikiTank"

    allowed_domains = ["wiki.warthunder.com"]

    # rootfolder = Path(__file__).parents[2]
    # f = open(rootfolder.as_posix() + "/tank_list")

    # Add all nation root pages
    def start_requests(self):
        urls = [
            "https://wiki.warthunder.com/Category:USA_ground_vehicles",
            "https://wiki.warthunder.com/Category:Germany_ground_vehicles",
            "https://wiki.warthunder.com/Category:USSR_ground_vehicles",
            "https://wiki.warthunder.com/Category:Britain_ground_vehicles",
            "https://wiki.warthunder.com/Category:Japan_ground_vehicles",
            "https://wiki.warthunder.com/Category:China_ground_vehicles",
            "https://wiki.warthunder.com/Category:Italy_ground_vehicles",
            "https://wiki.warthunder.com/Category:France_ground_vehicles",
            "https://wiki.warthunder.com/Category:Sweden_ground_vehicles",
            "https://wiki.warthunder.com/Category:Israel_ground_vehicles"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Go through all vehicles in the tech trees
    def parse(self, response):
        divs = response.xpath("//div[@class=$val]", val='tree')

        for domain in self.allowed_domains:    
            for a in divs.xpath(".//a/@href").extract():
                url = "https://" + domain + a
                yield scrapy.Request(url=url, callback=self.parse_vehicle)


    def parse_vehicle(self, response):
        vehicle_name = response.xpath("//div[@class=$val]/text()", val="general_info_name").get()
        
        info = response.xpath("//div[@class=$val]/div", val="general_info")

        nation = info[0].xpath(".//a/text()").get()
        rank = info[1].xpath(".//a/text()").get()

        info = response.xpath("//div[@class=$val]", val="general_info_2")
        
        real_br = info.xpath(".//td").getall()[-2]
        tank_type = info.xpath(".//div[@class=$val]/div/a/text()", val="general_info_class").get()

        # Get art image if it exists
        # Else get garage image
        img_link = response.xpath("//a[@class='image']/img[contains(@src, 'ArtImage')]/@src").getall()
        
        if len(img_link) == 0:
            img_link = response.xpath("//a[@class='image']/img[contains(@src, 'GarageImage')]/@src").get()
        else:
            img_link = img_link[0]

        yield {
            'Name': vehicle_name,
            'Nation': nation,
            'Rank': rank,
            'BR': real_br,
            'Type': tank_type,
            'Image': img_link
        }