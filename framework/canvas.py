from .colorthief import Smart_ColorThief
from PIL import Image, ImageFont, ImageDraw
from aiohttp import ClientSession
from io import BytesIO
import gc

class ServerCard:
    def __init__(self, ctx, font_path: str, session: ClientSession = None):
        """ Server Info command thingy """
        self.ctx = ctx

        self._use_new_session = session is None
        self._get_font = (lambda x: ImageFont.truetype(font_path, x))
        self._session = ClientSession() if self._use_new_session else session
        self._server_tier_urls = [
            "https://vierofernando.is-inside.me/YWs1Qw2q.png",
            "https://vierofernando.is-inside.me/BIe3ccYA.png",
            "https://vierofernando.is-inside.me/2vKUVwwM.png",
            "https://vierofernando.is-inside.me/T0sfEdj1.png"
        ]

    async def imagefromURL(self, url: str) -> Image:
        res = await self._session.get(url)
        res = await res.read()
        return Image.open(BytesIO(res))

    async def draw(self):
        """ draws teh card """
        # commenting everything because codes with comments make it look "tidier" :^)

        # get the guild icon
        server_icon = await self.imagefromURL(str(self.ctx.guild.icon_url_as(format="png", size=128)))
        server_icon = server_icon.resize((128, 128))
        _colorthief = Smart_ColorThief(self.ctx, str(self.ctx.guild.icon_url_as(format="png", size=128)))

        # colors !!!
        background_color = await _colorthief.get_color()
        foreground_color = (0, 0, 0) if (sum(background_color) // 3) > 128 else (255, 255, 255)
        lower_brightness = (lambda x: tuple(map(lambda h: h - x, background_color)))

        # get the text and font for the image
        big_font = self._get_font(30)
        sub_font = self._get_font(20)
        description = f"Created by {str(self.ctx.guild.owner)} at {str(self.ctx.guild.created_at)[:-7]}"

        # configure the image
        width = max([
            big_font.getsize(self.ctx.guild.name)[0] + 50,
            sub_font.getsize(description)[0]
        ]) + 208
        im = Image.new(mode="RGB", size=(width, 168), color=background_color)
        draw = ImageDraw.Draw(im)
        
        # paste the icon
        if server_icon.mode == "RGBA":
            im.paste(server_icon, (20, 20), server_icon)
        else:
            im.paste(server_icon, (20, 20))
        
        # create the rectangles
        draw.rectangle([(148, 20), (im.width - 20, 70)], fill=lower_brightness(50))
        draw.rectangle([(148, 70), (im.width - 20, 148)], fill=lower_brightness(70))

        tier_icon = await self.imagefromURL(self._server_tier_urls[self.ctx.guild.premium_tier])
        tier_icon = tier_icon.resize((40, 40))
        im.paste(tier_icon, (im.width - 75, 25), tier_icon)

        # draw those goddamn text smh
        draw.text((168, 20), self.ctx.guild.name, fill=foreground_color, font=big_font)
        draw.text((168, 75), description, fill=foreground_color, font=sub_font)
        draw.text((168, 103), f"{self.ctx.guild.member_count:,} members", fill=foreground_color, font=sub_font)
        text_length = sub_font.getsize(f"{self.ctx.guild.premium_subscription_count:,} boosters")[0]
        draw.text((im.width - 40 - text_length, 103), f"{self.ctx.guild.premium_subscription_count:,} boosters", fill=foreground_color, font=sub_font)

        # save to a buffer
        b = BytesIO()
        im.save(b, format="png")
        b.seek(0)

        # close the session if session is not defined in the beginning
        if self._use_new_session:
            await self._session.close()

        # delete to free memory
        del (
            im,
            draw,
            width,
            tier_icon,
            server_icon,
            text_length,
            big_font,
            sub_font,
            _colorthief,
            description,
            background_color,
            foreground_color,
            lower_brightness,
            self.ctx.guild,
            self._get_font,
            self._use_new_session,
            self._server_tier_urls
        )
        
        # collect those stinky memory garbage
        gc.collect()
        
        # return the buffer, complete !
        return b