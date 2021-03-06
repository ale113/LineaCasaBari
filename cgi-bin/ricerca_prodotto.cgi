#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;
use File::Basename;

my $cgi=new CGI;
my $session = CGI::Session->load();
if ($session->is_empty) {
	print $cgi->redirect('check_session.cgi?gestione_prodotti');
}
print $cgi->header('text/html');
my $email=$session->param("email");


my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
my $cod;
if ($ENV{'REQUEST_METHOD'} eq 'POST')
{
	$cod=param("codice");
	
}
else
{
	$cod=$ENV{'QUERY_STRING'};
}
my $messaggio="false";


if($ENV{'QUERY_STRING'}eq "modified")
{
	$messaggio="modifica effettuata con successo";
}
elsif($ENV{'QUERY_STRING'}eq "deleted")
{
	$messaggio="eliminazione effettuata con successo";
}
elsif (-e "../data/Prodotti.xml")
{
	my $parser=XML::LibXML->new;
	my $doc=$parser->parse_file("../data/Prodotti.xml");
	my @cod_prodotti=$doc->findnodes("Prodotti/Prodotto/Codice/text()");
	if(@cod_prodotti)
	{
		if($cod>=0)
		{
			my $i;
			foreach $i (@cod_prodotti)
			{
				if($i ne $cod)
				{
					$messaggio="il codice inserito non corrisponde a nessun prodotto esistente";
				}
				else
				{
					$messaggio="false";
					last;
				}
			}
		}
		else
		{
			$messaggio="inserisci un codice per la ricerca";
		}
	}
	else
	{
		$messaggio="non ci sono prodotti";
	}
}
else
{
	$messaggio="non ci sono prodotti";
}
my $vars;

if($messaggio eq "false")
{
	my $parser=XML::LibXML->new;
	my $doc=$parser->parse_file("../data/Prodotti.xml");
	push my @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Nome/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Descrizione/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Categoria/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Prezzo/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Data_aggiunta/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Valutazione/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Immagine/text()");
	my $num_tag=$doc->findvalue("count(Prodotti/Prodotto[Codice='$cod']/Tag)");
	for(my $x=1; $x<=$num_tag;$x++)
	{
		push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Tag[$x]/text()");
	}
	
	
	my $tot;
	my $i=0;
	
	my$x='<li>
        <label for="nome">Nome:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input id="nome" class="input" name="Nome" type="text" value="'."@prodotto[$i]".'" /></div><div class="inputRight"></div>
    </li>';
	$tot=$tot.$x;
	$i++;
	
	$x='<li>
        <label for="descrizione">Descrizione:</label><textarea id="descrizione" class="gestione_textarea" name="Descrizione">'."@prodotto[$i]".'</textarea>
    </li>';
	$i++;
	$tot=$tot.$x;
	
	my @splitstring= (split (/_/, basename(@prodotto[$i])));
	$x='<li><label for="categoria">La categoria &egrave;: '."@splitstring".'. Scegli la nuova:</label><select id="categoria" name="Categoria"><option value="lista_nozze"';
	$tot=$tot.$x;
	if(@prodotto[$i] eq "lista_nozze") {
		$x=' selected="selected"';
		$tot=$tot.$x;
	}
	$x='>Lista nozze</option><option value="porcellane"';
	$tot=$tot.$x;
	if(@prodotto[$i] eq "porcellane") {
		$x=' selected="selected"';
		$tot=$tot.$x;
	}
	$x='>Porcellane</option><option value="paralumi"';
	$tot=$tot.$x;
	if(@prodotto[$i] eq "paralumi") {
		$x=' selected="selected"';
		$tot=$tot.$x;
	}
	$x='>Paralumi</option><option value="pentole"';
	$tot=$tot.$x;
	if(@prodotto[$i] eq "pentole") {
		$x=' selected="selected"';
		$tot=$tot.$x;
	}
	$x='>Pentole</option><option value="per_la_tavola"';
	$tot=$tot.$x;
	if(@prodotto[$i] eq "per_la_tavola") {
		$x=' selected="selected"';
		$tot=$tot.$x;
	}
	$x='>Per la tavola</option><option value="tovaglie"';
	$tot=$tot.$x;
	if(@prodotto[$i] eq "tovaglie") {
		$x=' selected="selected"';
		$tot=$tot.$x;
	}
	$x='>Tovaglie</option></select></li>';
	$tot=$tot.$x;
	$i++;
	
	$x='<li>
        <label for="prezzo">Prezzo &#40;&#8364;&#41;: </label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input id="prezzo" class="input" name="Prezzo" type="text" value="'."@prodotto[$i]".'" /></div><div class="inputRight"></div>
    </li>';
	$tot=$tot.$x;
	$i++;
	
	$x='<li>
        <label for="data">Data aggiunta:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input id="data" class="input" name="Data" type="text" value="'."@prodotto[$i]".'" /></div><div class="inputRight"></div>
    </li>';
	$tot=$tot.$x;
	$i++;
	$i++;	
	
	my $filespec="@prodotto[$i]";
	my $path= dirname $filespec;
	my $filename=basename $filespec;
	my $read_directory="../images/prodotti";
	my $immagine="$read_directory/$filename";
	$x='<li>
        <label for="immagine" id="gestione-file_label">Inserisci una nuova immagine (dimensione massima 200kB):</label><img id="gestione-immagine_prodotto" src="'."$immagine".'" alt="foto prodotto" /><input id="immagine" type="file" name="Immagine" />
    </li>';
	$tot=$tot.$x;
	$i++;
		
	$x='<li>
        <label for="tag1">Tag:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input id="tag1" class="input" name="Tag1" type="text" value="'."@prodotto[$i]".'" /></div><div class="inputRight"></div>
    </li>';
	$i++;
	$tot=$tot.$x;
	
	$x='<li>
        <label for="tag2">Tag:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input id="tag2" class="input" name="Tag2" type="text" value="'."@prodotto[$i]".'" /></div><div class="inputRight"></div>
    </li>';
	$i++;
	$tot=$tot.$x;
	
	$x='<li>
        <label for="tag3">Tag:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input id="tag3" class="input" name="Tag3" type="text" value="'."@prodotto[$i]".'" /></div><div class="inputRight"></div>
    </li>';
	$i++;
	$tot=$tot.$x;
	
	$x='<li>
            <label for="tag4">Tag:</label>
            <div class="inputLeft"></div><div class="gestione-inputMiddle"><input id="tag4" class="input" name="Tag4" type="text" value="'."@prodotto[$i]".'" /></div><div class="inputRight"></div>
        </li>';
	$i++;
	$tot=$tot.$x;
	
	my $lista_prodotto='<div class="generic-container"><div class="form-container2"><form id="editProdottoForm" class="side-element" action="edit_prodotto.cgi" method="post" onsubmit="return editProdottoFunzione()"  enctype="multipart/form-data"><ul class="form-Block">'."$tot".'</ul><div class="side-element"><button class="button" type="submit">Modifica</button><input type="hidden" name="old_cod" value="'."$cod".'"/><input type="hidden" name="old_image" value="'."$filespec".'"/></div></form><form class="side-element" action="togli_prodotto.cgi" method="post"><div class="side-element"><input type="hidden" name="prodotto" value="'."$cod".'" /><button class="button" type="submit">Rimuovi</button></div></form></div></div>';
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "true",
		'lista_prodotti' => $lista_prodotto,
		'pagina' => "rimuovi_modifica",
	};
}
else
{
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "false",
		'messaggio_confirm' => $messaggio,
		'pagina' => "rimuovi_modifica",
		
		
	};
}
my $file='gestione_prodotti_temp.html';
$template->process($file,$vars) || die $template->error();
