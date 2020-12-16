from .colorthief import Smart_ColorThief
from PIL import Image, ImageFont, ImageDraw
from aiohttp import ClientSession
from time import time
from discord import ActivityType, File
from io import BytesIO
from twemoji_parser import emoji_to_url
import gc

class UserCard:
    def __init__(self, ctx, member, font_path: str, session = None):
        self.ctx = ctx
        self.user = member
        self.new_session = session is None
        self.font_path = font_path
        self.session = session if session else ClientSession()
        self.flags = {
            "nitro": "https://discordia.me/uploads/badges/nitro_badge.png",
            "booster": "https://erisly.com/assets/img/premium/boost.cb45e94.png",
            "badges": {
                "bug_hunter": "https://discordia.me/uploads/badges/bug_hunter_badge.png",
                "early_supporter": "https://discordia.me/uploads/badges/early_supporter_badge.png",
                "hypesquad_balance": "https://discordia.me/uploads/badges/balance_badge.png",
                "hypesquad_bravery": "https://discordia.me/uploads/badges/bravery_badge.png",
                "hypesquad_brilliance": "https://discordia.me/uploads/badges/brilliance_badge.png",
                "partner": "https://discordia.me/uploads/badges/partner_badge.png",
                "staff": "https://discordia.me/uploads/badges/staff_badge.png",
                "verified_bot_developer": "https://discordia.me/uploads/badges/verified_developer_badge.png"
            }
        }
    
    async def get_status_image(self):
        dict_data = self.user.activity.to_dict()
        
        if dict_data.get("emoji"):
            if dict_data["emoji"].get("id"):
                return f'https://cdn.discordapp.com/emojis/{dict_data["emoji"]["id"]}'
            emoji_url = await emoji_to_url(str(self.user.activity.emoji), session=self.session)
            if emoji_url.startswith("http"):
                return emoji_url
            return
        elif hasattr(self.user.activity, "album_cover_url"):
            return self.user.activity.album_cover_url
        elif dict_data.get("assets"):
            return f'https://cdn.discordapp.com/app-assets/{dict_data["application_id"]}/{dict_data["assets"]["small_image"]}.png'
        else:
            return
    
    def get_status_name(self):
        if self.user.activity.type == ActivityType.custom:
            return "<custom activity>"
        elif self.user.activity.type == ActivityType.listening:
            name = "Listening to "
        elif self.user.activity.type == ActivityType.competing:
            name = "Competing in "
        elif self.user.activity.type == ActivityType.watching:
            name = "Watching "
        elif self.user.activity.type == ActivityType.playing:
            name = "Playing "
        elif self.user.activity.type == ActivityType.streaming:
            name = "Streaming"
        else:
            return "???"
        
        return name + self.user.activity.to_dict()["name"]
    
    def get_font(self, size: int):
        return ImageFont.truetype(self.font_path, size)
    
    async def imagefromURL(self, url):
        resp = await self.session.get(url)
        resp = await resp.read()
        return Image.open(BytesIO(resp))
    
    async def send(self):
        # user avatar
        avatar = await self.imagefromURL(str(self.user.avatar_url_as(format="png", size=128)))
        avatar = avatar.resize((150, 150))
        
        # configure stuff
        _thief = Smart_ColorThief(self.ctx, str(self.user.avatar_url_as(format="png", size=128)))
        background_color = await _thief.get_color(right=True)
        foreground_color = (0, 0, 0) if (sum(background_color) // 3) > 128 else (255, 255, 255)
        lower_brightness = (lambda x: tuple(map(lambda y: y - x, background_color)))
        big_font = self.get_font(40)
        smol_font = self.get_font(25)
        tiny_font = self.get_font(20)
        title_size = big_font.getsize(self.user.display_name)[0]
        description = f"Created at {str(self.user.created_at)[:-7]} ({self.ctx.bot.util.strfsecond(time() - self.user.created_at.timestamp())} ago)" + "\n" + f"Joined at {str(self.user.joined_at)[:-7]} (Position: {self.ctx.bot.util.join_position(self.ctx.guild, self.user):,}/{self.ctx.guild.member_count:,})"
        del _thief
        
        # measure the width for the image
        width = max([
            title_size + tiny_font.getsize(f"#{self.user.discriminator}")[0] + 45,
            smol_font.getsize_multiline(description)[0] + 40
        ]) + 190
        
        # declare the main object
        main = Image.new(mode="RGB", size=(width, (230 if self.user.activity else 190)), color=background_color)
        draw = ImageDraw.Draw(main)
        
        # paste the avatar, if it's RGBA, paste it with transparent
        if avatar.mode == "RGBA":
            main.paste(avatar, (20, 20), avatar)
        else:
            main.paste(avatar, (20, 20))
        
        # draw main two rectangles
        draw.rectangle([(170, 20), (main.width - 20, 80)], fill=lower_brightness(20))
        draw.rectangle([(170, 80), (main.width - 20, 170)], fill=lower_brightness(40))
        
        # draw main text
        draw.text((190, 15), self.user.display_name, font=big_font, fill=foreground_color)
        draw.text((195 + title_size, 38), f"#{self.user.discriminator}", font=tiny_font, fill=foreground_color)
        draw.text((190, 85), description, font=smol_font, fill=foreground_color)

        # check if user has activity, then create another section for the activity
        if self.user.activity:
            url = await self.get_status_image()
            color = None if url else (255, 255, 255)
            
            if url:
                status_image = await self.imagefromURL(url)
                status_image = status_image.resize((40, 40)).convert("RGBA") if url.startswith("https://twemoji.maxcdn.com/") else status_image.resize((40, 40))
                _thief = Smart_ColorThief(self.ctx, url)
                activity_color = await _thief.get_color(right=True)
                
                draw.rectangle([(20, 170), (main.width - 20, 210)], fill=activity_color)
                color = (0, 0, 0) if ((sum(activity_color) // 3) > 128) else (255, 255, 255)
                
                if status_image.mode == "RGBA":
                    main.paste(status_image, (20, 170), status_image)
                else:
                    main.paste(status_image, (20, 170))
                del status_image, _thief, activity_color
            else:
                draw.rectangle([(20, 170), (main.width - 20, 210)], fill=(0, 0, 0))
            
            draw.text((70 - (0 if url else 40), 170), self.get_status_name(), font=smol_font, fill=color)
            del url, color
        
        # check and draw badges if user has one
        flag_y = main.width - 60
        for flag in self.flags["badges"].keys():
            if not getattr(self.user.public_flags, flag):
                continue
            
            flag_image = await self.imagefromURL(self.flags["badges"][flag])
            flag_image = flag_image.resize((30, 30))
            main.paste(flag_image, (flag_y, 30), flag_image)
            del flag_image
            flag_y -= 35
        
        # add nitro badge to list if user has one
        if self.ctx.bot.util.has_nitro(self.ctx.guild, self.user):
            flag_image = await self.imagefromURL(self.flags["nitro"])
            flag_image = flag_image.resize((30, 30))
            main.paste(flag_image, (flag_y, 30), flag_image)
            del flag_image
            flag_y -= 35
        
        # add booster badge to list if user has one
        if self.user in self.ctx.guild.premium_subscribers:
            flag_image = await self.imagefromURL(self.flags["booster"])
            flag_image = flag_image.resize((30, 30))
            main.paste(flag_image, (flag_y, 30), flag_image)
            del flag_image
        
        # save it to a buffer and send it
        b = BytesIO()
        main.save(b, format="png")
        b.seek(0)
        await self.ctx.send(file=File(b, "card.png"))
        
        # close the session if it was not previously defined
        if self.new_session:
            await self.session.close()
        
        # delete all the attributes
        del (
            main,
            draw,
            big_font,
            smol_font,
            tiny_font,
            width,
            description,
            lower_brightness,
            background_color,
            foreground_color,
            avatar,
            flag_y,
            self.flags,
            title_size,
            self.user,
            self.ctx,
            self.session,
            self.new_session,
            self.font_path,
            b
        )
        
        # collect the trash, ew
        gc.collect()

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
        server_icon = await self.imagefromURL(str(self.ctx.guild.icon_url_as(format="png", size=128)) if self.ctx.guild.icon_url else "https://cdn.discordapp.com/embed/avatars/0.png")
        server_icon = server_icon.resize((128, 128))
        _colorthief = Smart_ColorThief(self.ctx, str(self.ctx.guild.icon_url_as(format="png", size=128)) if self.ctx.guild.icon_url else "https://cdn.discordapp.com/embed/avatars/0.png")

        # colors !!!
        background_color = await _colorthief.get_color(right=True)
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