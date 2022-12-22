from flask.cli import with_appcontext
from webapp.api.models.Users import User, UserSchema
from webapp.api.models.Articles import Article, ArticleSchema
from webapp.api.utils import responses as resp
from webapp.api.utils.responses import response_with


@with_appcontext
def seed():
    """Seed the database."""
    try:
        # seed user admin
        adminexist = 0
        fetch = User.query.all()
        existinguserschema = UserSchema(
            many=True,
            only=[
                "iduser",
                "username",
                "email",
            ],
        )
        existinguser = existinguserschema.dump(fetch)
        for item in existinguser:
            if item["username"] == "admin":
                adminexist = 1
        if adminexist == 0:
            seeddata = {
                "username": "admin",
                "first_name": "Admin",
                "last_name": "KartUNS",
                "email": "admin@kartuns.org",
                "is_alumni": 1,
                "password": "4Dm1n",
                "is_admin": 1,
            }
            user_schema = (
                UserSchema()
            )  # user schema pertama didefinisikan full utk menerima seluruh data yang diperlukan termasuk password
            user = user_schema.load(seeddata)
            # need validation in user creation process (cek existing username, email, etc)
            userobj = User(
                username=user["username"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                email=user["email"],
                is_alumni=user["is_alumni"],
            )
            userobj.set_password(user["password"])
            userobj.is_admin = user["is_admin"]
            userobj.avatar(48)
            userobj.create()
            user_schema = UserSchema(
                only=["username", "first_name", "last_name", "email", "is_admin"]
            )  # definisikan ulang user_schema tanpa memasukkan plain password sehingga di exclude dari result/API response
            result = user_schema.dump(user)
            return response_with(
                resp.SUCCESS_201,
                value={
                    "status": "success",
                    "user": result,
                    "message": "An account has been created for {} successfully!".format(
                        user["email"]
                    ),
                },
            )
        # seed user pengurus
        adapengurus = 0
        fetch = User.query.all()
        existinguser = existinguserschema.dump(fetch)
        for item in existinguser:
            if item["username"] == "pengurus":
                adapengurus = 1
        if adapengurus == 0:
            seeddata = {
                "username": "pengurus",
                "first_name": "Pengurus",
                "last_name": "KartUNS",
                "email": "pengurus@kartuns.org",
                "is_alumni": 1,
                "password": "P3ngurU5",
                "is_admin": 0,
                "is_pengurus": 1,
            }
            user_schema = (
                UserSchema()
            )
            user = user_schema.load(seeddata)
            userobj = User(
                username=user["username"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                email=user["email"],
                is_alumni=user["is_alumni"],
            )
            userobj.set_password(user["password"])
            userobj.is_pengurus = user["is_pengurus"]
            userobj.is_alumni = user["is_alumni"]
            userobj.is_admin = user["is_admin"]
            userobj.avatar(48)
            userobj.create()

        # seed artikel (generate article using ChatGPT)
        # artikel #1
        artikelexist = 0
        fetch = Article.query.all()
        existingartikelschema = ArticleSchema(
            many=True,
            only=[
                "idarticle",
                "articletitle",
            ],
        )
        existingartikel = existingartikelschema.dump(fetch)
        for item in existingartikel:
            if item["articletitle"] == "Munas Keluarga Alumni Arsitektur UNS KartUNS Tahun 2022 Berlangsung Sukses":
                artikelexist = 1
        if artikelexist == 0:
            seeddata = {
                "articletitle": "Munas Keluarga Alumni Arsitektur UNS KartUNS Tahun 2022 Berlangsung Sukses",
                "articleimgurl": "upload_4155830841.JPG",
                "articledesc": "Munas Keluarga Alumni Arsitektur Universitas Sebelas Maret (UNS) atau yang lebih dikenal dengan KartUNS telah berlangsung dengan sukses pada akhir pekan lalu. Acara yang merupakan pertemuan tahunan bagi para alumni Arsitektur UNS ini diadakan di Gedung Rektorat UNS Surakarta dan dihadiri oleh sekitar 200 alumni yang tersebar di berbagai penjuru Indonesia.",
                "articletext": "<p>Munas Keluarga Alumni Arsitektur Universitas Sebelas Maret (UNS) atau yang lebih dikenal dengan KartUNS telah berlangsung dengan sukses pada akhir pekan lalu. Acara yang merupakan pertemuan tahunan bagi para alumni Arsitektur UNS ini diadakan di Gedung Rektorat UNS Surakarta dan dihadiri oleh sekitar 200 alumni yang tersebar di berbagai penjuru Indonesia.</p><p>Acara dimulai dengan sambutan dari Ketua panitia, Bapak Muhammad Zaki, yang menyambut para alumni yang hadir dan menyampaikan apa yang akan dilakukan selama acara berlangsung. Setelah itu, acara dilanjutkan dengan sesi sharing dan diskusi mengenai perkembangan arsitektur di Indonesia serta kesempatan bagi para alumni untuk saling bertukar pengalaman dan ide-ide kreatif. Selain itu, acara juga menghadirkan beberapa pembicara yang merupakan tokoh-tokoh penting di dunia arsitektur Indonesia, seperti Bapak Agus Dermawan, seorang arsitek ternama yang telah berpengalaman lebih dari 30 tahun di bidangnya, serta Ibu Rini Widowati, arsitek muda yang sedang naik daun dan telah menyelesaikan beberapa proyek besar di berbagai kota di Indonesia.</p><p>Tidak hanya itu, acara juga menyuguhkan beberapa kegiatan menyenangkan bagi para alumni seperti foto bersama, games, dan doorprize yang tentunya menambah suasana acara semakin meriah. Selain itu, para alumni juga diberikan kesempatan untuk berkeliling di kampus UNS dan melihat kembali tempat-tempat yang pernah mereka kunjungi selama kuliah.</p><p>Acara munas keluarga alumni arsitektur UNS ini diakui sebagai salah satu acara yang paling sukses dalam sejarah KartUNS. Para alumni yang hadir terlihat sangat antusias dan merasa terhibur dengan acara yang disuguhkan. Mereka juga terlihat senang bisa bertemu kembali dengan teman-teman lama dan saling bertukar pengalaman serta ide-ide kreatif.</p><p>Dalam sambutannya, Bapak Muhammad Zaki, ketua panitia acara, mengucapkan terima kasih kepada seluruh alumni yang hadir serta berharap agar acara munas keluarga alumni arsitektur UNS ini dapat terus dilaksanakan setiap tahunnya dan menjadi ajang silaturahmi bagi para alumni Arsitektur UNS.</p>",
            }
            artikel_schema = (
                ArticleSchema()
            )
            artikel = artikel_schema.load(seeddata)
            artikelobj = Article(
                articletitle=artikel["articletitle"],
                articledesc=artikel["articledesc"],
                articleimgurl=artikel["articleimgurl"],
                articletext=artikel["articletext"],
            )
            artikelobj.create()

        # artikel #2
        artikelexist = 0
        fetch = Article.query.all()
        existingartikelschema = ArticleSchema(
            many=True,
            only=[
                "idarticle",
                "articletitle",
            ],
        )
        existingartikel = existingartikelschema.dump(fetch)
        for item in existingartikel:
            if item["articletitle"] == "Arsitek Alumni UNS Memenangkan Berbagai Sayembara Arsitektur Tahun 2022":
                artikelexist = 1
        if artikelexist == 0:
            seeddata = {
                "articletitle": "Arsitek Alumni UNS Memenangkan Berbagai Sayembara Arsitektur Tahun 2022",
                "articleimgurl": "upload_4155830841.JPG",
                "articledesc": "Tahun 2022 memang menjadi tahun yang sangat menggembirakan bagi para alumni Arsitektur Universitas Sebelas Maret (UNS). Berbagai sayembara arsitektur di Indonesia telah dipenuhi oleh para alumni UNS yang memenangkan berbagai penghargaan dan pengakuan dari para juri.",
                "articletext": "<p>Tahun 2022 telah menjadi tahun yang luar biasa bagi para arsitek alumni Universitas Sebelas Maret (UNS). Berbagai sayembara arsitektur telah diadakan di seluruh Indonesia, dan para arsitek alumni UNS tersebut berhasil memenangkan banyak di antaranya. Ini merupakan prestasi yang sangat luar biasa dan tentunya menjadi suatu kebanggaan bagi para arsitek alumni UNS tersebut.</p><p>Namun, tidak hanya itu saja, prestasi tersebut juga merupakan inspirasi bagi para arsitek muda lainnya yang sedang meniti karier di dunia arsitektur. Para arsitek alumni UNS tersebut telah menunjukkan bahwa dengan kerja keras dan kemampuan yang dimiliki, seseorang dapat mencapai kesuksesan di bidang yang dipilihnya.</p><p>Mereka juga telah memberikan bukti bahwa Universitas Sebelas Maret merupakan salah satu perguruan tinggi terbaik di Indonesia yang dapat menghasilkan arsitek-arsitek handal dan berprestasi. Keberhasilan para arsitek alumni UNS tersebut juga merupakan bukti bahwa arsitektur Indonesia telah mampu bersaing dengan arsitektur dunia. Mereka telah membuktikan bahwa arsitektur Indonesia tidak hanya memiliki nilai estetika yang tinggi, tetapi juga mampu memberikan solusi yang inovatif dan sesuai dengan kebutuhan masyarakat.</p><p>Para arsitek alumni UNS tersebut juga telah memberikan sumbangsih yang besar bagi perkembangan arsitektur Indonesia. Mereka telah menciptakan berbagai bangunan yang memiliki nilai estetika tinggi, sesuai dengan kebutuhan masyarakat, serta mampu menjawab tantangan lingkungan dan iklim. Dengan prestasi yang telah dicapai oleh para arsitek alumni UNS tersebut, kita sebagai masyarakat Indonesia dapat terinspirasi untuk terus belajar dan berusaha mencapai kesuksesan di bidang yang dipilih.</p><p>Kita juga dapat bangga dengan prestasi yang telah dicapai oleh para arsitek alumni UNS tersebut, dan terus memberikan dukungan kepada mereka agar dapat terus berkarya dan memberikan sumbangsih yang lebih besar bagi perkembangan arsitektur Indonesia.</p>",
            }
            artikel_schema = (
                ArticleSchema()
            )
            artikel = artikel_schema.load(seeddata)
            artikelobj = Article(
                articletitle=artikel["articletitle"],
                articledesc=artikel["articledesc"],
                articleimgurl=artikel["articleimgurl"],
                articletext=artikel["articletext"],
            )
            artikelobj.create()

        # artikel #3

        # seed cover

    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)
